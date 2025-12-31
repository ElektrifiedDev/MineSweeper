import random as rand
import os
from colorama import Fore, Style, init
from collections import deque

init(autoreset=True)

def setup_game():
    global GRID_SIZE, NUM_MINES
    while True:
        try:
            GRID_SIZE = int(input("Enter grid length (5-25): "))
            if 5 <= GRID_SIZE <= 25:
                break
            print("PLEASE ENTER A NUMBER BETWEEN 5 AND 25.")
        except ValueError:
            print("PLEASE ENTER A VALID WHOLE NUMBER.")
    
    NUM_MINES = (GRID_SIZE * GRID_SIZE) // 5
    return GRID_SIZE, NUM_MINES

def create_board():
    return [[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]

def place_mines(board, safe_row, safe_col):
    mines = 0
    while mines < NUM_MINES:
        row = rand.randint(0, GRID_SIZE - 1)
        col = rand.randint(0, GRID_SIZE - 1)
        if board[row][col] != "[M]" and (row != safe_row or col != safe_col):
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
    colors = {
        "[X]": Fore.LIGHTBLACK_EX, "[F]": Fore.LIGHTRED_EX, "[M]": Fore.RED,
        "[0]": Fore.WHITE, "[1]": Fore.BLUE, "[2]": Fore.GREEN,
        "[3]": Fore.YELLOW, "[4]": Fore.MAGENTA, "[5]": Fore.CYAN,
        "[6]": Fore.LIGHTRED_EX, "[7]": Fore.LIGHTBLUE_EX, "[8]": Fore.LIGHTGREEN_EX
    }
    return colors.get(cell, "") + cell + Style.RESET_ALL

def print_board(board, revealed, flagged, mines_left):
    print(f"\n   MINES REMAINING: {mines_left}")
    print("     " + "".join([str(i).center(3) for i in range(GRID_SIZE)]))
    print("   --" + "---" * GRID_SIZE)
    for i, row in enumerate(board):
        row_display = []
        for j, cell in enumerate(row):
            if flagged[i][j]:
                row_display.append(color_cell("[F]"))
            elif revealed[i][j]:
                row_display.append(color_cell(str(cell)))
            else:
                row_display.append(color_cell("[X]"))
        print(f"{str(i).rjust(2)} | {''.join(row_display)}")

def flood_reveal(board, revealed, row, col):
    queue = deque([(row, col)])
    while queue:
        r, c = queue.popleft()
        if revealed[r][c]: continue
        revealed[r][c] = True
        if board[r][c] == "[0]":
            for i in range(max(0, r - 1), min(GRID_SIZE, r + 2)):
                for j in range(max(0, c - 1), min(GRID_SIZE, c + 2)):
                    if not revealed[i][j]:
                        queue.append((i, j))

def play_game():
    setup_game()
    board = create_board()
    revealed = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    flagged = [[False for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
    
    first_move = True
    flags_placed = 0

    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        mines_left = NUM_MINES - flags_placed
        print_board(board, revealed, flagged, mines_left)
        
        user_input = input("\n'r c' to reveal | 'F r c' to flag: ").split()

        if not user_input: continue

        if user_input[0].upper() == 'F' and len(user_input) == 3:
            try:
                row, col = map(int, user_input[1:])
                if not revealed[row][col]:
                    if flagged[row][col]:
                        flagged[row][col] = False
                        flags_placed -= 1
                    else:
                        if flags_placed < NUM_MINES:
                            flagged[row][col] = True
                            flags_placed += 1
                        else:
                            input("OUT OF FLAGS! Unflag another square first.")
            except (ValueError, IndexError):
                input("Invalid input. Press Enter...")
            continue

        try:
            row, col = map(int, user_input)
            if flagged[row][col]:
                input("Cell is flagged! Unflag it first.")
                continue
            
            if first_move:
                place_mines(board, row, col)
                update_numbers(board)
                first_move = False
            
            if board[row][col] == "[M]":
                os.system('cls' if os.name == 'nt' else 'clear')
                print_board(board, [[True]*GRID_SIZE for _ in range(GRID_SIZE)], flagged, 0)
                print(Fore.RED + "BOOM! GAME OVER.")
                break
                
            flood_reveal(board, revealed, row, col)
        except (ValueError, IndexError):
            input("Invalid input. Press Enter...")
            continue

        safe_tiles_revealed = all(
            revealed[r][c] or board[r][c] == "[M]"
            for r in range(GRID_SIZE) for c in range(GRID_SIZE)
        )
        
        correct_flags = sum(1 for r in range(GRID_SIZE) for c in range(GRID_SIZE) 
                           if flagged[r][c] and board[r][c] == "[M]")

        if safe_tiles_revealed and correct_flags == NUM_MINES:
            os.system('cls' if os.name == 'nt' else 'clear')
            print_board(board, revealed, flagged, 0)
            print(Fore.GREEN + "CONGRATULATIONS! BOARD CLEARED.")
            break

    input("\nPress Enter to exit...")

if __name__ == "__main__":
    play_game()