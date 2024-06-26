import math

# Constants
PLAYER1 = 'X'
PLAYER2 = 'O'
EMPTY = ' '

def print_board(board):
    for row in board:
        print('|'.join(row))
        print('-' * 5)

def check_winner(board, player):
    # Check rows
    for row in board:
        if all([cell == player for cell in row]):
            return True
    # Check columns
    for col in range(3):
        if all([board[row][col] == player for row in range(3)]):
            return True
    # Check diagonals
    if all([board[i][i] == player for i in range(3)]):
        return True
    if all([board[i][2-i] == player for i in range(3)]):
        return True
    return False

def is_full(board):
    return all([cell != EMPTY for row in board for cell in row])

def evaluate(board):
    if check_winner(board, PLAYER2):
        return 1
    elif check_winner(board, PLAYER1):
        return -1
    else:
        return 0

def minimax(board, depth, alpha, beta, is_maximizing):
    score = evaluate(board)
    if score == 1 or score == -1:
        return score
    if is_full(board):
        return 0

    if is_maximizing:
        max_eval = -math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER2
                    eval = minimax(board, depth + 1, alpha, beta, False)
                    board[i][j] = EMPTY
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
        return max_eval
    else:
        min_eval = math.inf
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER1
                    eval = minimax(board, depth + 1, alpha, beta, True)
                    board[i][j] = EMPTY
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
        return min_eval

def best_move(board, player):
    best_val = -math.inf if player == PLAYER2 else math.inf
    move = (-1, -1)
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = player
                move_val = minimax(board, 0, -math.inf, math.inf, player == PLAYER1)
                board[i][j] = EMPTY
                if (player == PLAYER2 and move_val > best_val) or (player == PLAYER1 and move_val < best_val):
                    move = (i, j)
                    best_val = move_val
    return move

def get_valid_move(board):
    while True:
        try:
            move = input("Enter your move (row and column, e.g., 1 1): ").split()
            if len(move) != 2:
                raise ValueError
            row, col = int(move[0]), int(move[1])
            if row < 0 or row > 2 or col < 0 or col > 2:
                raise ValueError
            if board[row][col] != EMPTY:
                print("The cell is not empty. Try again.")
                continue
            return row, col
        except ValueError:
            print("Invalid input. Please enter two numbers between 0 and 2.")

def play():
    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    current_player = PLAYER1

    while True:
        print_board(board)
        if current_player == PLAYER1:
            row, col = get_valid_move(board)
            board[row][col] = PLAYER1
            if check_winner(board, PLAYER1):
                print_board(board)
                print("Player 1 wins!")
                break
            current_player = PLAYER2
        else:
            row, col = get_valid_move(board)
            board[row][col] = PLAYER2
            if check_winner(board, PLAYER2):
                print_board(board)
                print("Player 2 wins!")
                break
            current_player = PLAYER1

        if is_full(board):
            print_board(board)
            print("It's a tie!")
            break

        # Optional hint for the current player using Minimax
        hint_row, hint_col = best_move(board, current_player)
        print(f"Hint for Player {current_player}: Consider placing at ({hint_row}, {hint_col})")

if __name__ == "__main__":
    play()
