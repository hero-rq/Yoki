"""
Problem Statement:

Write a Python program that can solve a maze represented by a 2D grid. The maze consists of open cells 
(represented by 0) and walls (represented by 1). The program should find a path from the top-left corner 
of the maze (start) to the bottom-right corner (end) using Depth-First Search (DFS) or Breadth-First Search 
(BFS). If a path exists, it should return the path; otherwise, it should indicate that no path exists.
"""

def drawing_path(maze, path):
    """
    Draws the path found on the maze.
    """
    for (x, y) in path:
        maze[x][y] = 5  # visualize the program finding the route as '5' 

    return maze

def is_valid_move(maze, x, y, visited):
    """
    Check if the move to cell (x, y) is valid.
    """
    n, m = len(maze), len(maze[0])
    return 0 <= x < n and 0 <= y < m and maze[x][y] == 0 and (x, y) not in visited

def find_path(maze):
    """
    Find a path from the top-left corner to the bottom-right corner of the maze.
    """
    start = (0, 0)
    end = (len(maze) - 1, len(maze[0]) - 1)
    path = []
    visited = set()
    
    def dfs(x, y):
        if (x, y) == end:
            path.append((x, y))
            return True
        
        if not is_valid_move(maze, x, y, visited):
            return False
        
        visited.add((x, y))
        path.append((x, y))
        
        # Explore neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if dfs(x + dx, y + dy):
                return True
        
        path.pop()
        return False

    if dfs(start[0], start[1]):
        return path
    else:
        return None


target_maze = [
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 1, 0, 1, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 1, 1, 0],
    [0, 1, 1, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 1, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0]
]

for row in target_maze:
    print(row)
print("\nThis is the target maze\n")    

result = find_path(target_maze)
if result:
    print("Path found:", result)
    solved_maze = drawing_path(target_maze, result)  
    for row in solved_maze:
        print(row)
else:
    print("No path found")
