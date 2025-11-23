"""
You get a list of numbers.
Find the longest stretch of numbers (contiguous) whose sum is even.
Return the length. If none exist, return 0.
"""

from typing import List


def longest_even_sum_subarray(nums: List[int]) -> int:
    if not nums:
        return 0

    check_list = []

    for start in range(len(nums)):
        current_sum = 0
        best_length = 0
        for end in range(start, len(nums)):
            current_sum += nums[end]
            if current_sum % 2 == 0:
                best_length += 1
        check_list.append(best_length)

    return max(check_list)


def run_manual_examples() -> None:
    test_cases = [
        ([1, 2, 3, 4], 4),
        ([1, 3, 5], 0),
        ([2, 2, 2], 3),
        ([1], 0),
        ([2], 1),
        ([1, 2, 2, 1], 4),
    ]

    print("Running manual test cases...\n")
    for nums, expected in test_cases:
        result = longest_even_sum_subarray(nums)
        print(f"Input: {nums}")
        print(f"Expected: {expected}, Got: {result}")
        print("-" * 40)


def main():
    print("Longest Even-Sum Subarray Checker")
    user_input = input("Enter numbers: ").strip()

    if user_input == "":
        run_manual_examples()
    else:
        try:
            nums = [int(x) for x in user_input.split()]
        except ValueError:
            print("Invalid input.")
            return

        result = longest_even_sum_subarray(nums)
        print(f"\nResult: {result}")


if __name__ == "__main__":
    main()
