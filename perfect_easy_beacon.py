def count_2x2_hash_squares(grid):
    if not grid or not grid[0]:
        return 0

    rows = len(grid)
    cols = len(grid[0])
    count = 0

    for i in range(rows - 1):
        for j in range(cols - 1):
            if (grid[i][j] == "#" and
                grid[i][j+1] == "#" and
                grid[i+1][j] == "#" and
                grid[i+1][j+1] == "#"):
                count += 1

    return count


# Test Case
grid_map = [
    ['#', '#', '.', '#', '#'],
    ['#', '#', '.', '#', '#'],
    ['.', '.', '.', '.', '.'],
    ['#', '#', '.', '.', '.']
]

print(count_2x2_hash_squares(grid_map))  # 2
