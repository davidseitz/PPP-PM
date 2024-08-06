"""
This is the main function of the program.
It initializes the menu and starts the program execution.
"""
import menu

def main() -> None:
    menu.curses.wrapper(menu.main)
    
if __name__ == "__main__":
    main()