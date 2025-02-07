import pygame
import sys
import random

# -------------------- Configuration --------------------
BOARD_SIZE = 9            # 9x9 board for simplicity
CELL_SIZE = 60            # Distance between intersections (in pixels)
MARGIN = 40               # Margin around the board (in pixels)
WINDOW_SIZE = MARGIN * 2 + CELL_SIZE * (BOARD_SIZE - 1)
FPS = 30                  # Frames per second

# Board representation:
# 0 -> empty, 1 -> Black (human), 2 -> White (computer)

# -------------------- Helper Functions --------------------
def get_neighbors(row, col, board_size):
    """Return adjacent board coordinates (up, down, left, right)."""
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))
    if row < board_size - 1:
        neighbors.append((row + 1, col))
    if col > 0:
        neighbors.append((row, col - 1))
    if col < board_size - 1:
        neighbors.append((row, col + 1))
    return neighbors

def get_group_and_liberties(board, row, col):
    """
    Given a board and a starting position, return the full group of connected
    stones (same color) and a set of adjacent empty positions (liberties).
    """
    color = board[row][col]
    group = set()
    liberties = set()
    stack = [(row, col)]
    while stack:
        r, c = stack.pop()
        if (r, c) in group:
            continue
        group.add((r, c))
        for nr, nc in get_neighbors(r, c, len(board)):
            if board[nr][nc] == 0:
                liberties.add((nr, nc))
            elif board[nr][nc] == color and (nr, nc) not in group:
                stack.append((nr, nc))
    return group, liberties

def remove_group(board, group):
    """Remove a captured group of stones from the board."""
    for r, c in group:
        board[r][c] = 0

def apply_move(board, row, col, color):
    """
    Try to apply a move for the given color at (row, col).
    Returns a new board state if the move is legal (after removing any captures),
    or None if the move is illegal.
    """
    # Copy the board to simulate the move.
    new_board = [r[:] for r in board]
    if new_board[row][col] != 0:
        return None  # The cell is already occupied.
    new_board[row][col] = color
    enemy_color = 2 if color == 1 else 1

    # Check enemy neighbors for possible capture.
    for nr, nc in get_neighbors(row, col, len(board)):
        if new_board[nr][nc] == enemy_color:
            group, liberties = get_group_and_liberties(new_board, nr, nc)
            if len(liberties) == 0:
                remove_group(new_board, group)

    # Check if the newly placed stone's group has any liberties.
    group, liberties = get_group_and_liberties(new_board, row, col)
    if len(liberties) == 0:
        # Illegal move (suicide) if no liberties remain.
        return None

    return new_board

def get_all_legal_moves(board, color):
    """Return a list of all legal moves (row, col) for the given color."""
    moves = []
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == 0:
                new_board = apply_move(board, r, c, color)
                if new_board is not None:
                    moves.append((r, c))
    return moves

def computer_move(board, color):
    """Compute a legal move for the computer (random selection)."""
    legal_moves = get_all_legal_moves(board, color)
    if legal_moves:
        move = random.choice(legal_moves)
        new_board = apply_move(board, move[0], move[1], color)
        return new_board, move
    else:
        return board, None  # No legal move; the computer passes.

def pixel_to_board(x, y):
    """
    Convert pixel coordinates (x, y) to the nearest board intersection.
    Returns (row, col) or None if outside the board area.
    """
    board_col = round((x - MARGIN) / CELL_SIZE)
    board_row = round((y - MARGIN) / CELL_SIZE)
    if board_col < 0 or board_col >= BOARD_SIZE or board_row < 0 or board_row >= BOARD_SIZE:
        return None
    # Compute the exact center of the intersection.
    center_x = MARGIN + board_col * CELL_SIZE
    center_y = MARGIN + board_row * CELL_SIZE
    # Check if the click is close enough.
    if abs(x - center_x) < CELL_SIZE / 2 and abs(y - center_y) < CELL_SIZE / 2:
        return board_row, board_col
    return None

def draw_board(screen, board):
    """Render the Go board and stones."""
    # Fill the background with a wood-like color.
    screen.fill((222, 184, 135))
    # Draw grid lines.
    for i in range(BOARD_SIZE):
        start_pos = (MARGIN, MARGIN + i * CELL_SIZE)
        end_pos = (MARGIN + (BOARD_SIZE - 1) * CELL_SIZE, MARGIN + i * CELL_SIZE)
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)
    for j in range(BOARD_SIZE):
        start_pos = (MARGIN + j * CELL_SIZE, MARGIN)
        end_pos = (MARGIN + j * CELL_SIZE, MARGIN + (BOARD_SIZE - 1) * CELL_SIZE)
        pygame.draw.line(screen, (0, 0, 0), start_pos, end_pos, 2)
    # Draw stones.
    for r in range(BOARD_SIZE):
        for c in range(BOARD_SIZE):
            if board[r][c] != 0:
                center = (MARGIN + c * CELL_SIZE, MARGIN + r * CELL_SIZE)
                if board[r][c] == 1:
                    stone_color = (0, 0, 0)
                else:
                    stone_color = (255, 255, 255)
                pygame.draw.circle(screen, stone_color, center, CELL_SIZE // 2 - 2)
                # Add a black outline for white stones.
                if board[r][c] == 2:
                    pygame.draw.circle(screen, (0, 0, 0), center, CELL_SIZE // 2 - 2, 2)
    pygame.display.flip()

# -------------------- Main Game Loop --------------------
def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
    pygame.display.set_caption("Local Go (Baduk) Game")
    clock = pygame.time.Clock()

    # Initialize an empty board.
    board = [[0 for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    current_player = 1  # 1 for human (Black), 2 for computer (White)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Human (Black) makes a move.
                if current_player == 1:
                    pos = pygame.mouse.get_pos()
                    move = pixel_to_board(pos[0], pos[1])
                    if move:
                        r, c = move
                        new_board = apply_move(board, r, c, current_player)
                        if new_board is not None:
                            board = new_board
                            current_player = 2
                        else:
                            print("Illegal move!")
        # Computer (White) makes a move.
        if current_player == 2:
            pygame.time.wait(500)  # Pause briefly for a natural feel.
            board, comp_move = computer_move(board, current_player)
            if comp_move is not None:
                print(f"Computer played at {comp_move}")
            else:
                print("Computer passes (no legal moves).")
            current_player = 1

        draw_board(screen, board)
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()
