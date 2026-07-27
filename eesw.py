from typing import List, Dict, Any

def navigate_desert(
    start_pos: List[int], 
    moves: str, 
    sand_traps: List[List[int]]
) -> Dict[str, Any]:
    
    curr_row, curr_col = start_pos
    
    # Fast lookup for sand traps
    traps_set = set(tuple(trap) for trap in sand_traps)
    
    # Unique visited squares (automatically starts with 1 chest for start position)
    visited = {(curr_row, curr_col)}
    
    # Direction offsets: (delta_row, delta_col)
    direction_offsets = {
        'N': (-1, 0),
        'S': (1, 0),
        'E': (0, 1),
        'W': (0, -1)
    }
    
    for move in moves.upper():
        if move in direction_offsets:
            dr, dc = direction_offsets[move]
            
            # 1. Calculate target position FIRST
            next_row = curr_row + dr
            next_col = curr_col + dc
            
            # 2. Check if target is a Sand Trap
            if (next_row, next_col) in traps_set:
                continue  # Skip move, remain at (curr_row, curr_col)
            
            # 3. Valid move! Update current position and record square
            curr_row, curr_col = next_row, next_col
            visited.add((curr_row, curr_col))
            
    return {
        "final_pos": [curr_row, curr_col],
        "chests": len(visited)  # Total unique squares visited
    }


# --- Testing Examples ---

# Example 1
res1 = navigate_desert(start_pos=[0, 0], moves="EESW", sand_traps=[[0, 2]])
print("Example 1 Output:", res1)
# Output: {'final_pos': [1, 0], 'chests': 4}

# Example 2
res2 = navigate_desert(start_pos=[2, 2], moves="NNSS", sand_traps=[])
print("Example 2 Output:", res2)
# Output: {'final_pos': [2, 2], 'chests': 3}
