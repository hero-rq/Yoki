#!/usr/bin/env python3
import socket
import sys

def is_prime(n: int) -> bool:
    """Deterministic Miller–Rabin for n < 2^64"""
    if n < 2:
        return False
    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        if n % p == 0:
            return n == p
    d, s = n - 1, 0
    while d % 2 == 0:
        d //= 2
        s += 1
    for a in (2, 325, 9375, 28178, 450775, 9780504, 1795265022):
        x = pow(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(s - 1):
            x = (x * x) % n
            if x == n - 1:
                break
        else:
            return False
    return True

def fetch_numbers(host: str, port: int):
    """Connect, receive all data, return list of ints"""
    with socket.create_connection((host, port), timeout=10) as sock:
        data = b''
        while True:
            chunk = sock.recv(4096)
            if not chunk:
                break
            data += chunk
    text = data.decode('utf-8', errors='ignore')
    nums = [int(tok) for tok in text.split() if tok.strip().lstrip('-').isdigit()]
    return nums, text, sock

def main():
    HOST = '94.237.51.163'
    PORT = 44277

    try:
        nums, greeting, sock = fetch_numbers(HOST, PORT)
    except Exception as e:
        print(f"✖ could not fetch data: {e}", file=sys.stderr)
        sys.exit(1)

    print("Received:\n" + "="*40)
    print(greeting)
    print("="*40)

    primes = [n for n in nums if is_prime(n)]
    if len(primes) != 2:
        print(f"✖ expected exactly 2 primes, found {len(primes)}: {primes}", file=sys.stderr)
        sys.exit(1)

    p, q = primes
    key = p * q
    print(f"Primes found: {p}, {q}")
    print(f"Computed key = {p} × {q} = {key}")

    with socket.create_connection((HOST, PORT), timeout=10) as s2:
        s2.sendall(f"{key}\n".encode())
        reply = s2.recv(4096).decode('utf-8', errors='ignore')
        print("Server reply:")
        print(reply)

if __name__ == '__main__':
    main()
