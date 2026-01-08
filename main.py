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

def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')

def main_menu():
    while True:
        clear_console()
        print(Fore.CYAN + "=== Main Menu ===")
        print("1. Start New Game")
        print("2. Exit")
        choice = input("Select an option: ")
        if choice == '1':
            return
        elif choice == '2':
            sys.exit()
        else:
            print(Fore.RED + "Invalid choice. Please try again.")
            time.sleep(2)

def resize_window(board_size):
    cols = max(50, (board_size * 4) + 10)
    lines = max(25, board_size + 12)
    resize_terminal(cols, lines)

def resize_terminal(cols, rows):
    sys.stdout.write(f"\x1b[8;{rows};{cols}t")
    sys.stdout.flush()

def board_size():
    board_size = 10
    return board_size

def color_cell(cell):
    colors = {
        "[X]": Fore.LIGHTBLACK_EX, "[F]": Fore.LIGHTRED_EX, "[M]": Fore.RED,
        "[0]": Fore.WHITE, "[1]": Fore.BLUE, "[2]": Fore.GREEN,
        "[3]": Fore.YELLOW, "[4]": Fore.MAGENTA, "[5]": Fore.CYAN,
        "[6]": Fore.LIGHTRED_EX, "[7]": Fore.LIGHTBLUE_EX, "[8]": Fore.LIGHTGREEN_EX
    }
    return colors.get(cell, "") + cell + Style.RESET_ALL

def create_board(board_size):
    return [[0 for _ in range(board_size)] for _ in range(board_size)]

def main_game_loop():
    main_menu()
    board_size_value = board_size()
    board = create_board(board_size_value)
    resize_window(board_size_value)
    clear_console()