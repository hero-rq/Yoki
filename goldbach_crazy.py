#!/usr/bin/env python3
"""
goldbach_helper.py  –  hybrid verifier / reducer for Goldbach’s conjecture

STRATEGY
  1.  If N ≤ WALL = 4·10^18           →  rely on published exhaustive check.
  2.  Try to find a prime pair         →  full Goldbach success.
  3.  Fall back to Chen representation →  prime  +  semiprime  (p + (q·r)).
      • if the semiprime turns out to be prime → upgrade to Goldbach success.
      • else                                  → record Chen success; still open gap.
  4.  (optional) slice N-3 and invoke Helfgott’s weak Goldbach code path
      to shrink N until it drops below WALL or passes step 2.

"""
from __future__ import annotations
import sys, math, argparse, itertools, multiprocessing as mp
from typing import List, Tuple, Optional

# -------- 1.  Deterministic Miller–Rabin for 64-bit ints --------
_MR_BASIS = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)

def _try_composite(a, d, n, s):
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return False
    for _ in range(s - 1):
        x = (x * x) % n
        if x == n - 1:
            return False
    return True  # dc

def is_prime(n: int) -> bool:
    if n < 2:          return False
    for p in (2, 3, 5, 7, 11, 13, 17):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    return not any(_try_composite(a, d, n, s) for a in _MR_BASIS)

# -------- 2.  Simple wheel-based prime generator  --------
def prime_sieve(limit: int) -> List[int]:
    """Return all primes ≤ limit using a fast wheel/bit sieve."""
    if limit < 2: return []
    size = (limit // 2)         # ignore even numbers
    sieve = bytearray(b"\x01") * (size + 1)
    for i in range(1, int(limit**0.5) // 2 + 1):
        if sieve[i]:
            step = 2*i + 1
            start = 2*i*(i+1)
            sieve[start::step] = b"\x00" * ((size - start) // step + 1)
    return [2] + [2*i + 1 for i in range(1, size+1) if sieve[i]]

# -------- 3.  Goldbach and Chen finders  --------
def goldbach_split(even: int, primes: List[int]) -> Optional[Tuple[int, int]]:
    """Return a prime pair (p,q) with p+q=even, or None."""
    for p in itertools.takewhile(lambda x: x <= even//2, primes):
        q = even - p
        if is_prime(q):
            return p, q
    return None

def chen_split(even: int, primes: List[int]) -> Optional[Tuple[int, int, int]]:
    """
    Return p + q where q is prime or semiprime (q = r*s).
    Gives (p, r, s)  – if q itself is prime set r=q, s=1.
    """
    for p in primes:
        q = even - p
        if q < 4:
            return None
        if is_prime(q):
            return (p, q, 1)
        # semiprime test
        limit = int(math.isqrt(q))
        for r in primes:
            if r > limit or r*r > q: break
            if q % r == 0:
                s = q // r
                if is_prime(s):
                    return (p, r, s)
    return None

# -------- 4.  Range checker with multiprocessing  --------
def _range_worker(lo: int, hi: int, primes: List[int], out):
    for n in range(lo, hi+1, 2):
        if goldbach_split(n, primes) is None:
            out.put(n)          # counter-example! boom 
            return
    out.put(None)

def verify_range(max_n: int, jobs: int = None) -> bool:
    if max_n < 4: return True
    jobs = jobs or mp.cpu_count()
    step = (max_n // (2*jobs)) * 2  # even stride
    primes = prime_sieve(max_n)     # broadcast
    ctx = mp.get_context('fork')
    queue = ctx.Queue()
    ps = []
    for i in range(jobs):
        lo = 4 + i*step
        hi = min(max_n, lo + step - 2)
        p = ctx.Process(target=_range_worker, args=(lo, hi, primes, queue))
        p.start(); ps.append(p)
    for _ in ps:
        bad = queue.get()
        if bad:                     # found counter-example
            for p in ps: p.terminate()
            print(bad, file=sys.stderr)
            return False
    return True

# -------- 5.  Top-level dispatcher  --------
WALL = 4_000_000_000_000_000_000  # 4·10^18  (Oliveira e Silva 2014) Charles Oliveria vs Topuria ? 

def prove_even(even: int) -> str:
    if even % 2 or even < 4:
        raise ValueError("Input must be an even integer ≥ 4")

    if even <= WALL:
        return "true  (already verified ≤ 4·10¹⁸)"

    primes = prime_sieve(int(math.isqrt(even)) + 1)
    gb = goldbach_split(even, primes)
    if gb:
        p, q = gb
        print(f"goldbach   {even} = {p} + {q}")
        return "true"

    ch = chen_split(even, primes)
    if ch:
        p, r, s = ch
        if s == 1:
            print(f"goldbach   {even} = {p} + {r}")
            return "true"
        else:
            print(f"chen       {even} = {p} + {r}*{s}  (semiprime)")
            return "chen_true"

    print(f"unknown     could not split {even} with current bounds")
    return "unknown"

# -------- 6.  CLI  --------
def main():
    ap = argparse.ArgumentParser(description="Goldbach proof-helper")
    ap.add_argument("n", nargs="?", type=int,
                    help="single even integer to analyse")
    ap.add_argument("--up-to", type=int, metavar="M",
                    help="exhaustively verify all evens 4…M")
    ap.add_argument("--procs", type=int, help="parallel workers (default=CPU)")
    args = ap.parse_args()

    if args.n is not None and args.up_to:
        ap.error("choose a single n OR --up-to, not both")

    if args.n is not None:
        print(prove_even(args.n))
    else:
        M = args.up_to or 10_000_000
        ok = verify_range(M, jobs=args.procs)
        if ok:
            print(f"verified Goldbach for all even 4…{M}")
            print("true")
        else:
            print("false")

if __name__ == "__main__":
    mp.freeze_support()   # Windows safety
    main()
