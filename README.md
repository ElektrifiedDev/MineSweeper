# Minesweeper

Official page of [ElektrifiedDev](https://github.com/ElektrifiedDev)'s [Minesweeper](https://github.com/ElektrifiedDev/Minesweeper)! This is a fully functional, terminal-based version of the classic puzzle game


# How To Play
This game runs directly in your Windows Command Line

## Reveal a Cell
Type the row number and column number seperated by a space (for example: `4 9`; this would go to the Row 4 (Fifth Row) and the Column 9(Tenth Column)) to reveal a cell. 
Note: The numerical offset is due to how digital indexing works.

## Flag a Cell
Type `F` followed by the coordinates (e.g., `F 2 3`) to mark a suspected mine.

## Win Condition
Reveal all cells that do not contain mines to win the game. Revealing a cell that contains a mine will cause you to lose the game.


# Key Features

## Flood Revealing
An Algorithm so that whenever a `[0]` is revealed, surrounding numbers will also be instantly revealed.

## Color-Coded Interface
Uses `colorama` to highlight different numbers, flags and mines for better readability.

## Portable Executable
Bundled into a standalone `.exe` to ensure it can run without needing Python installed. Go to the [Releases Page](https://github.com/ElektrifiedDev/Minesweeper/releases) to find these.


# Technical Specifications
- **Build Environment**: Python 3.14
- **File Size**: Approximately 8 MB
- **Dependencies**: Built with `colorama` for terminal styling and packaged with `PyInstaller`
