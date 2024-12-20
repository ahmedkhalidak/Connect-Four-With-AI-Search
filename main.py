import numpy as np
import tkinter as tk
from tkinter import messagebox
import math
import random

ROW_COUNT = 6
COLUMN_COUNT = 7
PLAYER_PIECE = 1
AI_PIECE = 2
EMPTY = 0
WINDOW_LENGTH = 4
SQUARESIZE = 100

# Create the board 
def create_board():
    return np.zeros((ROW_COUNT, COLUMN_COUNT)) 

# Drop a piece 
def drop_piece(board, row, col, piece):
    board[row][col] = piece

# Check if the column is valid for a move
def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

# Get the next open row in the column
def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r
#----------------------------------------
# Check for a winning move 
def winning_move(board, piece):
    # Check horizontal locations
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r][c + 1] == piece
                and board[r][c + 2] == piece
                and board[r][c + 3] == piece
            ):
                return True

    # Check vertical locations
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c] == piece
                and board[r + 2][c] == piece
                and board[r + 3][c] == piece
            ):
                return True

    # Check positive diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if (
                board[r][c] == piece
                and board[r + 1][c + 1] == piece
                and board[r + 2][c + 2] == piece
                and board[r + 3][c + 3] == piece
            ):
                return True

    # Check negative diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if (
                board[r][c] == piece
                and board[r - 1][c + 1] == piece
                and board[r - 2][c + 2] == piece
                and board[r - 3][c + 3] == piece
            ):
                return True

    return False
#------------------------------------------
# Evaluate a window for scoring 
def evaluate_window(window, piece):
    score = 0
    opp_piece = PLAYER_PIECE if piece == AI_PIECE else AI_PIECE

    if window.count(piece) == 4:
        score += 100
    elif window.count(piece) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(piece) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opp_piece) == 3 and window.count(EMPTY) == 1:
        score -= 4

    return score

# Score the board
def score_position(board, piece):
    score = 0

    # Score center column
    center_array = [int(i) for i in list(board[:, COLUMN_COUNT // 2])]
    center_count = center_array.count(piece)
    score += center_count * 3

    # Score Horizontal
    for r in range(ROW_COUNT):
        row_array = [int(i) for i in list(board[r, :])]
        for c in range(COLUMN_COUNT - 3):
            window = row_array[c : c + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score Vertical
    for c in range(COLUMN_COUNT):
        col_array = [int(i) for i in list(board[:, c])]
        for r in range(ROW_COUNT - 3):
            window = col_array[r : r + WINDOW_LENGTH]
            score += evaluate_window(window, piece)

    # Score positive sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    # Score negative sloped diagonal
    for r in range(ROW_COUNT - 3):
        for c in range(COLUMN_COUNT - 3):
            window = [board[r + 3 - i][c + i] for i in range(WINDOW_LENGTH)]
            score += evaluate_window(window, piece)

    return score

# Check for terminal 
def is_terminal_node(board):
    return (
        winning_move(board, PLAYER_PIECE)
        or winning_move(board, AI_PIECE)
        or len(get_valid_locations(board)) == 0
    )
    
    
# Get valid locations 
def get_valid_locations(board):
    valid_locations = []
    for col in range(COLUMN_COUNT):
        if is_valid_location(board, col):
            valid_locations.append(col)
    return valid_locations

# Minimax algorithm
def minimax(board, depth, alpha, beta, maximizingPlayer): 
    valid_locations = get_valid_locations(board) 
    is_terminal = is_terminal_node(board)
    if depth == 0 or is_terminal:  
        if is_terminal:
            if winning_move(board, AI_PIECE):
                return (None, 100000000000000)
            elif winning_move(board, PLAYER_PIECE):
                return (None, -10000000000000)
            else:
                return (None, 0)
        else:
            return (None, score_position(board, AI_PIECE))

    if maximizingPlayer: 
        final_score = -math.inf 
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, AI_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, False)[1] 
            if new_score > final_score:
                final_score = new_score
                column = col
            alpha = max(alpha, final_score)
            if alpha >= beta:
                break
        return column, final_score

    else: 
        final_score = math.inf 
        column = random.choice(valid_locations)
        for col in valid_locations:
            row = get_next_open_row(board, col)
            b_copy = board.copy()
            drop_piece(b_copy, row, col, PLAYER_PIECE)
            new_score = minimax(b_copy, depth - 1, alpha, beta, True)[1]
            if new_score < final_score:
                final_score = new_score
                column = col
            beta = min(beta, final_score)
            if alpha >= beta:
                break
        return column, final_score

# Draw the board 
def draw_board():
    canvas.delete("all")
    for r in range(ROW_COUNT):
        for c in range(COLUMN_COUNT):
            color = "white"
            if board[r][c] == PLAYER_PIECE:
                color = "red"
            elif board[r][c] == AI_PIECE:
                color = "yellow"

            canvas.create_oval(
                c * SQUARESIZE + 5,
                (ROW_COUNT - r - 1) * SQUARESIZE + 5,
                (c + 1) * SQUARESIZE - 5,
                (ROW_COUNT - r) * SQUARESIZE - 5,
                fill=color,
            )

# Make a move  
def make_move(col):
    global turn
    if is_valid_location(board, col):
        row = get_next_open_row(board, col)
        drop_piece(board, row, col, PLAYER_PIECE if turn == 0 else AI_PIECE)

        draw_board()

        if winning_move(board, PLAYER_PIECE if turn == 0 else AI_PIECE):
            winner = "Player" if turn == 0 else "AI"
            messagebox.showinfo("Game Over", f"{winner} wins!")
            root.quit()

        turn = (turn + 1) % 2

        if turn == 1:
            ai_move()

# AI move 
def ai_move():
    col, minimax_score = minimax(board, 5, -math.inf, math.inf, True)
    make_move(col)


board = create_board()
turn = 0


root = tk.Tk()
root.title("Connect Four")

canvas = tk.Canvas(root, width=COLUMN_COUNT * SQUARESIZE, height=ROW_COUNT * SQUARESIZE, bg="blue")
canvas.pack()

draw_board()


button_frame = tk.Frame(root)
button_frame.pack()

buttons = []
for c in range(COLUMN_COUNT):
    button = tk.Button(
        button_frame, 
        text=f"Col {c+1}", 
        command=lambda col=c: make_move(col),
        width=8,  
        height=2,  
        font=("Arial", 10), 
        bg="lightgray"  
    )
    button.grid(row=0, column=c, padx=7, pady=5)

    buttons.append(button)



root.mainloop() 
