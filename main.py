import random as rand ## Importing random module for mine placement
import os ## Importing os module for clearing the console
from colorama import Fore, Style, init ## Importing colorama for colored text output
from collections import deque ## Importing deque for efficient flood fill algorithm

init(autoreset=True) ## Initialize colorama

# Setup game parameters
def setup_game():
    global GRID_SIZE, NUM_MINES
    while True:
        try:
            GRID_SIZE = int(input("Enter the desired length of the Minesweeper grid: ")) ## Size of the Minesweeper grid
            if GRID_SIZE < 5 or GRID_SIZE >= 30:
                print("PLEASE ENTER A NUMBER BETWEEN 5 AND 30 FOR THE BEST EXPERIENCE.")
                os.system('cls')
                continue
            else:
                break
        except ValueError:
            print("PLEASE ENTER A VALID WHOLE NUMBER.")
            os.system('cls')
            continue
    NUM_MINES = (GRID_SIZE * GRID_SIZE) // 5 ## Number of mines to place on the grid
    return GRID_SIZE, NUM_MINES

# Create the game board
def create_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

# Place mines randomly on the board
def place_mines(board):
    mines = 0
    while mines < NUM_MINES:
        row = rand.randint(0, GRID_SIZE - 1)
        col = rand.randint(0, GRID_SIZE - 1)
        if board[row][col] != "[M]":
            board[row][col] = "[M]"
            mines += 1

# Update the board with numbers indicating adjacent mines
def update_numbers(board):
    ## Calculates the number of adjacent mines for every non-mine cell on the board. 
    ## Iterates through a 3x3 grid around each cell to count [M] instances.
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == "[M]":
                continue
            count = 0
            for i in range(max(0, row - 1), min(GRID_SIZE, row + 2)):
                for j in range(max(0, col - 1), min(GRID_SIZE, col + 2)):
                    if board[i][j] == "[M]":
                        count += 1
            board[row][col] = f"[{count}]"

# Color the cell based on its content
def color_cell(cell):
    if cell == "[X]":
        return Fore.LIGHTBLACK_EX + cell + Style.RESET_ALL
    elif cell == "[F]":
        return Fore.LIGHTRED_EX + cell + Style.RESET_ALL
    elif cell == "[M]":
        return Fore.RED + cell + Style.RESET_ALL
    elif cell == "[0]":
        return Fore.WHITE + cell + Style.RESET_ALL
    elif cell == "[1]":
        return Fore.BLUE + cell + Style.RESET_ALL
    elif cell == "[2]":
        return Fore.GREEN + cell + Style.RESET_ALL
    elif cell == "[3]":
        return Fore.YELLOW + cell + Style.RESET_ALL
    elif cell == "[4]":
        return Fore.MAGENTA + cell + Style.RESET_ALL
    elif cell == "[5]":
        return Fore.CYAN + cell + Style.RESET_ALL
    elif cell == "[6]":
        return Fore.LIGHTRED_EX + cell + Style.RESET_ALL
    elif cell == "[7]":
        return Fore.LIGHTBLUE_EX + cell + Style.RESET_ALL
    elif cell == "[8]":
        return Fore.LIGHTGREEN_EX + cell + Style.RESET_ALL
    else:
        return cell

# Print the current state of the board
def print_board(board, revealed, flagged):
    print("     " + "".join([str(i).center(3) for i in range(GRID_SIZE)]))
    print("   --" + "---" * GRID_SIZE)
    for i, row in enumerate(board):
        row_display = []
        for j, cell in enumerate(row):
            if flagged[i][j]:
                row_display.append(color_cell(str("[F]")))
            elif revealed[i][j]:
                row_display.append(color_cell(str(cell)))
            else:
                row_display.append(color_cell("[X]"))
        print(f"{str(i).rjust(2)} | {''.join(row_display)}")

# Flood fill algorithm to reveal empty cells
def flood_reveal(board, revealed, row, col):
    # An efficient flood-fill algorithm using a deque (Breadth-First Search).
    # When a cell with [0] is revealed, it automatically expands to reveal 
    # all connected empty cells and their immediate numbered borders.
    queue = deque()
    queue.append((row, col))
    GRID = len(board)

    while queue:
        r, c = queue.popleft()

        # Already revealed? skip
        if revealed[r][c]:
            continue

        revealed[r][c] = True

        # Only expand if this is a zero
        if board[r][c] != "[0]":
            continue

        # Check neighbors
        for i in range(max(0, r - 1), min(GRID, r + 2)):
            for j in range(max(0, c - 1), min(GRID, c + 2)):
                if not revealed[i][j]:
                    queue.append((i, j))

# Main game loop
def play_game():
    setup_game()
    board = create_board()
    place_mines(board)
    update_numbers(board)

    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

    while True:
        os.system('cls')
        print_board(board, revealed, flagged)
        user_input = input("Enter row and column to reveal, or 'F row col' to flag: ").split()

        if len(user_input) == 2:  # reveal
            try:
                row, col = map(int, user_input)
            except ValueError:
                print("INVALID INPUT. PLEASE ENTER 2 NUMBERS OR USE 'F row col'.")
                input("Press Enter to continue...")
                continue
            if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
                print("INVALID CO-ORDINATES. TRY AGAIN.")
                input("Press Enter to continue...")
                continue
            if flagged[row][col]:
                print("You can't reveal a flagged cell. Unflag it first.")
                input("Press Enter to continue...")
                continue
            if board[row][col] == "[M]":
                os.system('cls')
                print_board(board, [[True]*GRID_SIZE for _ in range(GRID_SIZE)], flagged)
                print("BOOM! You hit a mine. GAME OVER.")
                break
            if board[row][col] == "[0]":
                flood_reveal(board, revealed, row, col)
            else:
                revealed[row][col] = True

        elif len(user_input) == 3 and user_input[0].upper() == 'F':  # flag toggle
            try:
                row, col = map(int, user_input[1:])
            except ValueError:
                print("INVALID INPUT. PLEASE ENTER 'F row col'.")
                input("Press Enter to continue...")
                continue
            if row < 0 or row >= GRID_SIZE or col < 0 or col >= GRID_SIZE:
                print("INVALID CO-ORDINATES. TRY AGAIN.")
                input("Press Enter to continue...")
                continue
            if revealed[row][col]:
                print("You can't flag a revealed cell.")
                input("Press Enter to continue...")
                continue
            flagged[row][col] = not flagged[row][col]

        else:
            print("INVALID COMMAND.")
            input("Press Enter to continue...")
            continue

        # Win condition: all non-mines revealed
        if all(
            revealed[r][c] or board[r][c] == "[M]"
            for r in range(GRID_SIZE)
            for c in range(GRID_SIZE)
        ):
            os.system('cls')
            print_board(board, revealed, flagged)
            print("Congratulations, You Beat The Board!")
            break

    input()

play_game()