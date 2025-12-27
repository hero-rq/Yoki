def is_palindrome(nums):
    n = len(nums)
    for i in range(n // 2):
        if nums[i] != nums[n - 1 - i]:
            return False
    return True


def find_mirror_core(heartbeats):
    n = len(heartbeats)
    best = []

    for start in range(n):
        for end in range(start + 1, n + 1):
            window = heartbeats[start:end]
            if len(window) > len(best) and is_palindrome(window):
                best = window

    return best

print(find_mirror_core([1, 2, 3, 2, 1, 9, 9])) # Expected: [1, 2, 3, 2, 1]
print(find_mirror_core([5, 6, 7, 8]))          # Expected: []
print(find_mirror_core([1, 2, 3, 2, 1, 1, 2, 3, 2, 1]))
