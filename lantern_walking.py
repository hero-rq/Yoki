from typing import List, Tuple

def decode_lantern_path(grid: List[str], moves: str) -> Tuple[str, int, int]:
    rows = len(grid)
    cols = len(grid[0]) if rows else 0

    # 1) FIND START AND END
    sr = sc = er = ec = 0
    for i in range(rows):
        for j in range(cols):
            if grid[i][j] == "S":
                sr, sc = i, j
            elif grid[i][j] == "E":
                er, ec = i, j

    # 2) INITIALIZE TRACKERS
    curr_r, curr_c = sr, sc
    visited = {(curr_r, curr_c)}
    first_reach_step = -1

    # 3) THE MOVE SIMULATION
    for step, move in enumerate(moves, start=1):
        next_r, next_c = curr_r, curr_c

        if move == 'U':
            next_r -= 1
        elif move == 'D':
            next_r += 1
        elif move == 'L':
            next_c -= 1
        elif move == 'R':
            next_c += 1

        is_inside = (0 <= next_r < rows) and (0 <= next_c < cols)

        if is_inside and grid[next_r][next_c] != '#':
            curr_r, curr_c = next_r, next_c

        visited.add((curr_r, curr_c))

        if (curr_r, curr_c) == (er, ec) and first_reach_step == -1:
            first_reach_step = step

    # 4) FINAL RESULTS
    status = "REACHED" if first_reach_step != -1 else "NOT REACHED"
    return status, len(visited), first_reach_step


if __name__ == "__main__":
    test_grid = ["S..", ".#.", "..E"]
    test_moves = "RRDD"
    print(decode_lantern_path(test_grid, test_moves))  # ("REACHED", 5, 4)
