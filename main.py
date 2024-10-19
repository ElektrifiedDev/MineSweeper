import random as rand

GRID_SIZE = 10
NUM_MINES = 20

def create_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def place_mines(board):
    mines = 0
    while mines < NUM_MINES:
        row = rand.randint(0, GRID_SIZE - 1)
        col = rand.randint(0, GRID_SIZE - 1)
        if board[row][col] != "M":
            board[row][col] = "M"
            mines += 1

def update_numbers(board):
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "M":
                continue
            count = 0
            for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
                for j in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
                    if board[i][j] == "M":
                        count += 1
            board[row][col] = f"[{count}]"

def print_board(board, revealed):
    print("   " + " ".join([str(i) for i in range(GRID_SIZE)]))
    print("  " + "---" * GRID_SIZE)
    for i, row in enumerate(board):
        row_display = []
        for j, cell in enumerate(row):
            if revealed[i][j]:
                row_display.append(str(cell))
            else:
                row_display.append("[X]")
        print(f"{i} | {''.join(row_display)}")

def play_game():
    board = create_board()
    place_mines(board)
    update_numbers(board)

    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    while True:
        print_board(board, revealed)
        try:
            row, col = map(int, input("Enter row and column to reveal:  ").split())
            if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
                print("INVALID CO-ORDINATES. TRY AGAIN.")
                continue
        except ValueError:
            print("INVALID INPUT. PLEASE ENTER 2 NUMBERS SEPERATED BY A SPACE.")
            continue
        if board[row][col] == "M":
            print("BOOM! You hit a mine. GAME OVER.")
            print_board(board, [[True] * GRID_SIZE for _ in range(GRID_SIZE)])
            break
        revealed[row][col] = True

        if all(revealed[r][c] or board[r][c] == "M" for r in range(GRID_SIZE) for c in range(GRID_SIZE)):
            print("Congratulations, You Beat The Board!")
            print_board(board, revealed)
            break
    input()


play_game()
