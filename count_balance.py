def count_balance_points(nums):
    total = sum(nums)
    left_sum = 0
    balance_count = 0

    for i in range(len(nums)):
        right_sum = total - left_sum - nums[i]

        if left_sum == right_sum:
            balance_count += 1

        left_sum += nums[i]

    return balance_count

nums = list(map(int, input().split()))
print(count_balance_points(nums))
