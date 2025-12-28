import random as rand
import os
from colorama import Fore, Style, init
init(autoreset=True)

GRID_SIZE = 10
NUM_MINES = 20

def create_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def place_mines(board):
    mines = 0
    while mines < NUM_MINES:
        row = rand.randint(0, GRID_SIZE - 1)
        col = rand.randint(0, GRID_SIZE - 1)
        if board[row][col] != "[M]":
            board[row][col] = "[M]"
            mines += 1

def update_numbers(board):
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

def print_board(board, revealed, flagged):
    print("     " + "  ".join([str(i) for i in range(GRID_SIZE)]))
    print("  --" + "---" * GRID_SIZE)
    for i, row in enumerate(board):
        row_display = []
        for j, cell in enumerate(row):
            if flagged[i][j]:
                row_display.append(color_cell(str("[F]")))
            elif revealed[i][j]:
                row_display.append(color_cell(str(cell)))
            else:
                row_display.append(color_cell("[X]"))
        print(f"{i} | {''.join(row_display)}")

def play_game():
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