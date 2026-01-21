def alpha_value_char(c: str) -> int:
    # assumes c is 'a'..'z'
    return ord(c) - 96

def mirror_swap_checksum(s: str, k: int) -> int:
    arr = list(s)
    n = len(arr)

    # perform k swaps: swap (i-1, n-i) for i = 1..k
    for i in range(1, k + 1):
        left = i - 1
        right = n - i
        arr[left], arr[right] = arr[right], arr[left]

    # compute checksum
    result = 0
    for idx, c in enumerate(arr):   # idx is 0-based
        result += (idx + 1) * alpha_value_char(c)

    return result

if __name__ == "__main__":
    print(mirror_swap_checksum("abcd", 2))  # 20
    print(mirror_swap_checksum("azby", 1))  # 87
