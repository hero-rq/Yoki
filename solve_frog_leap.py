def solve_frog_leap(stones):
    current_index = 0
    total_distance = 0
    visited_indices = set() 

    while 0 <= current_index < len(stones):
        if current_index in visited_indices:
            break

        visited_indices.add(current_index)
        jump = stones[current_index]

        if jump == 0:
            break

        total_distance += jump
        current_index += jump

    return total_distance


print(solve_frog_leap([2, 1, 3, 0, 5]))  # Output: 5
