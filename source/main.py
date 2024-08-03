"""
This is the main function of the program.
It initializes the menu and starts the program execution.
"""
from . import menu

def main() -> None:
    menu.curses.wrapper(menu.main)
    