from collections import deque

def solve():
    n, m = map(int, input().split())
    grid = [input().strip() for _ in range(n)]

    # visited[r][c][k] = True means we've reached (r,c) with k walls broken
    # k=0: no wall broken yet, k=1: one wall already broken
    visited = [[[False, False] for _ in range(m)] for _ in range(n)]

    # BFS: state = (row, col, walls_broken_so_far)
    queue = deque()

    # Handle start cell: if it's a wall, we use our one break on it
    start_breaks = 1 if grid[0][0] == '#' else 0
    if start_breaks <= 1:
        visited[0][0][start_breaks] = True
        queue.append((0, 0, start_breaks))

    while queue:
        r, c, breaks = queue.popleft()

        # Reached the goal
        if r == n - 1 and c == m - 1:
            print("YES")
            return

        # Only right or down
        for dr, dc in [(1, 0), (0, 1)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < n and 0 <= nc < m:
                cell_is_wall = grid[nr][nc] == '#'
                new_breaks = breaks + (1 if cell_is_wall else 0)

                if new_breaks <= 1 and not visited[nr][nc][new_breaks]:
                    visited[nr][nc][new_breaks] = True
                    queue.append((nr, nc, new_breaks))

    print("NO")

solve()
