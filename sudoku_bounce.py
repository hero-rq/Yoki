def find_empty_cell(board):
    for row in range(9):
        for col in range(9):
            if board[row][col] == 0:
                return row, col
    return None

def is_valid(board, row, col, num):
    for i in range(9):
        if board[row][i] == num:
            return False

    for i in range(9):
        if board[i][col] == num:
            return False

    start_row = (row // 3) * 3
    start_col = (col // 3) * 3
    for i in range(3):
        for j in range(3):
            if board[start_row + i][start_col + j] == num:
                return False

    return True

def solve_sudoku(board):
    empty_cell = find_empty_cell(board)
    if not empty_cell:
        return True  
    
    row, col = empty_cell

    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num  
            
            if solve_sudoku(board):
                return True  
            
            board[row][col] = 0 
    
    return False 

board = [
    [5, 3, 0, 0, 7, 0, 0, 0, 0],
    [6, 0, 0, 1, 9, 5, 0, 0, 0],
    [0, 9, 8, 0, 0, 0, 0, 6, 0],
    [8, 0, 0, 0, 6, 0, 0, 0, 3],
    [4, 0, 0, 8, 0, 3, 0, 0, 1],
    [7, 0, 0, 0, 2, 0, 0, 0, 6],
    [0, 6, 0, 0, 0, 0, 2, 8, 0],
    [0, 0, 0, 4, 1, 9, 0, 0, 5],
    [0, 0, 0, 0, 8, 0, 0, 7, 9]
]

board1 = [
    [0, 0, 0, 0, 0, 0, 0, 1, 0],
    [4, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 5, 0, 0, 0, 0, 8],
    [0, 0, 0, 2, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 3, 0, 0, 0],
    [3, 0, 0, 0, 0, 0, 4, 0, 7],
    [0, 0, 5, 0, 0, 0, 0, 7, 3],
    [0, 0, 0, 0, 8, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 6, 0, 0, 0]
]

board2 = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 7, 0, 0, 0, 0, 3, 0, 9],
    [3, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 0, 0, 0, 3, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 2, 0, 0],
    [8, 0, 1, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]

boards = [board, board1, board2]

for i in range(0, 3):
    for row in boards[i]:
        print(row)   
    print("raw board")
    print("\n")       
    if solve_sudoku(boards[i]):
        for row in boards[i]:
            print(row) 
        print("tamtamburin")
        print("\n")     
    else:
        print("No solution exists")
