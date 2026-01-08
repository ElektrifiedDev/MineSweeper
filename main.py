import random as rand
import collections
import os
import json
import sys
import time
import datetime
import colorama
import hashlib

from colorama import Fore, Style, init
from collections import deque

init(autoreset=True)

# --- Utility Functions ---
def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def resize_terminal(cols, rows):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()

def resize_window(board_size):
    cols = max(50, (board_size * 4) + 12)
    lines = max(10, board_size + 10)
    resize_terminal(cols, lines)

# --- Game Logic Functions ---
def board_size():
    return 10

def color_cell(cell):
    colors = {
        "[X]": Fore.LIGHTBLACK_EX, "[F]": Fore.LIGHTRED_EX, "[M]": Fore.RED,
        "[0]": Fore.WHITE, "[1]": Fore.BLUE, "[2]": Fore.GREEN,
        "[3]": Fore.YELLOW, "[4]": Fore.MAGENTA, "[5]": Fore.CYAN,
        "[6]": Fore.LIGHTRED_EX, "[7]": Fore.LIGHTBLUE_EX, "[8]": Fore.LIGHTGREEN_EX
    }
    return colors.get(cell, "") + cell + Style.RESET_ALL

def create_board(size):
    return [[0 for _ in range(size)] for _ in range(size)]

def place_mines(board, num_mines, size):
    mines = 0
    while mines < num_mines:
        row = rand.randint(0, size - 1)
        col = rand.randint(0, size - 1)
        if board[row][col] != "[M]":
            board[row][col] = "[M]"
            mines += 1
    return board

def update_numbers(board, size):
    for row in range(size):
        for col in range(size):
            if board[row][col] == "[M]":
                continue
            count = 0
            for i in range(max(0, row - 1), min(size, row + 2)):
                for j in range(max(0, col - 1), min(size, col + 2)):
                    if board[i][j] == "[M]":
                        count += 1
            board[row][col] = f"[{count}]"
    return board

def display_board(player_board, size):
    # Print column headers
    header = "   " + "".join([f"{i:2} " for i in range(size)])
    print(Fore.YELLOW + header)
    
    for r in range(size):
        # Print row header
        row_str = Fore.YELLOW + f"{r:2} " + Style.RESET_ALL
        for c in range(size):
            row_str += color_cell(player_board[r][c])
        print(row_str)

# --- Main Flow ---
def main_menu():
    while True:
        clear_console()
        print(Fore.CYAN + "=== CLI MINESWEEPER ===")
        print("1. Start New Game")
        print("2. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            return
        elif choice == '2':
            sys.exit()

def main_game_loop():
    main_menu()
    
    # Setup
    size = board_size()
    num_mines = int((size ** 2) // 5)
    
    # Internal board
    solution_board = create_board(size)
    solution_board = place_mines(solution_board, num_mines, size)
    solution_board = update_numbers(solution_board, size)
    
    # External board
    player_board = [["[X]" for _ in range(size)] for _ in range(size)]
    
    resize_window(size)
    game_over = False
    cells_to_clear = (size * size)

    while not game_over:
        clear_console()
        print(Fore.CYAN + f"Mines: {num_mines} | Cells left: {cells_to_clear}\n")
        display_board(player_board, size)
        
        try:
            prompt = input("\nEnter move (row col) or (f row col) to flag: ").lower().split()
            
            if not prompt: continue
            
            flagging = prompt[0] == 'f'
            if flagging:
                r, c = int(prompt[1]), int(prompt[2])
            else:
                r, c = int(prompt[0]), int(prompt[1])

            if not (0 <= r < size and 0 <= c < size):
                print(Fore.RED + "Out of bounds!")
                time.sleep(1)
                continue

            if flagging:
                if player_board[r][c] == "[X]":
                    player_board[r][c] = "[F]"
                elif player_board[r][c] == "[F]":
                    player_board[r][c] = "[X]"
                continue

            if player_board[r][c] != "[X]":
                print(Fore.YELLOW + "Already revealed or flagged!")
                time.sleep(1)
                continue

            # Check for mine
            if solution_board[r][c] == "[M]":
                clear_console()
                print(Fore.RED + "BOOM! Game Over.")
                display_board(solution_board, size) # Show solution
                game_over = True
            else:
                # Reveal cell
                player_board[r][c] = solution_board[r][c]
                cells_to_clear -= 1
                
                if cells_to_clear == 0:
                    clear_console()
                    print(Fore.GREEN + "Congratulations! You cleared the field!")
                    display_board(solution_board, size)
                    game_over = True

        except (ValueError, IndexError):
            print(Fore.RED + "Invalid input. Use 'r c' or 'f r c'.")
            time.sleep(1)

    input("\nPress Enter to return to menu...")
    main_game_loop()

if __name__ == "__main__":
    main_game_loop()