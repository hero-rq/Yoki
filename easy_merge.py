def mirror_merge(nums):
    """
    Apply the Mirror Merge rules until no merges are possible.
    Return the final list of integers.
    """
    i = 0
    while i < len(nums) - 1:
        if nums[i] == nums[i+1]:
            nums[i] += 1
            nums.pop(i + 1)
            i = 0
        else:
            i += 1
            
    return nums


def main():
    try:
        line1 = input().strip()
        if not line1:
            return
        n = int(line1)
        
        line2 = input().strip()
        if not line2:
            nums = []
        else:
            nums = list(map(int, line2.split()))
        
        result = mirror_merge(nums)
        print(" ".join(map(str, result)))
    except EOFError:
        pass


if __name__ == "__main__":
    main()
