def find_first_repeat(nums):
    k = []

    k = nums.copy()

    for i in range(len(k)):
        for j in range(i + 1, len(k)):
            if k[i] == k[j]:
                return k[i]
    return None

if __name__ == "__main__":
    nums = list(map(int, input().split()))
    result = find_first_repeat(nums)
    print(result if result is not None else "NONE")

