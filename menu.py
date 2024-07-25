import curses
import json
import os

def print_menu(stdscr, selected_row_idx, menu):
    stdscr.clear()
    h, w = stdscr.getmaxyx()

    for idx, row in enumerate(menu):
        x = w // 2 - len(row) // 2
        y = h // 2 - len(menu) // 2 + idx
        if idx == selected_row_idx:
            stdscr.attron(curses.color_pair(1))
            stdscr.addstr(y, x, row)
            stdscr.attroff(curses.color_pair(1))
        else:
            stdscr.addstr(y, x, row)
    stdscr.refresh()

def get_input(stdscr, prompt):
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, w // 2 - len(prompt) // 2, prompt)
    stdscr.refresh()

    input_win = curses.newwin(1, len(prompt) + 10, h // 2, w // 2 - len(prompt) // 2)
    curses.echo()  # Enable input echoing
    user_input = input_win.getstr().decode('utf-8')
    curses.noecho()  # Disable input echoing
    return user_input

def save_user(username, password):
    user_data = {
        "username": username,
        "password": password
    }

    if os.path.exists("user.json"):
        with open("user.json", "r") as file:
            users = json.load(file)
    else:
        users = []

    users.append(user_data)

    with open("user.json", "w") as file:
        json.dump(users, file, indent=4)

def login(stdscr):
    # Einloggen mit Username und Passwort
    temp1 = get_input(stdscr, "Please log in using your username and password. Press any key to continue.")
    username = get_input(stdscr, "Enter username: ")
    password = get_input(stdscr, "Enter password: ")

    stdscr.clear()
    stdscr.addstr(1, 0, f"Username: {username}")
    stdscr.addstr(2, 0, f"Password: {password}")
    stdscr.addstr(3, 0, "Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()

def register(stdscr):
    # Registrieren mit Username und Passwort
    temp1 = get_input(stdscr, "Please add a username and a password. Press any key to continue.")
    username = get_input(stdscr, "Enter username: ")
    password = get_input(stdscr, "Enter password: ")

    save_user(username, password)

    stdscr.clear()
    stdscr.addstr(1, 0, f"Username: {username}")
    stdscr.addstr(2, 0, f"Password: {password}")
    stdscr.addstr(3, 0, "New User Saved! Press any key to return to the menu.")
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    menu = ['Log In', 'New User', 'Exit']
    current_row_idx = 0

    while True:
        print_menu(stdscr, current_row_idx, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(menu) - 1:
            current_row_idx += 1
        elif key == ord('\n'):
            selected_option = menu[current_row_idx]
            if selected_option == 'Exit':
                break
            elif selected_option == 'Log In':
                login(stdscr)
            elif selected_option == 'New User':
                register(stdscr)
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, f"You selected '{selected_option}'.")
                stdscr.addstr(1, 0, "Press any key to return to the menu.")
                stdscr.refresh()
                stdscr.getch()
        print_menu(stdscr, current_row_idx, menu)

    stdscr.clear()
    stdscr.addstr(0, 0, "Goodbye!")
    stdscr.refresh()
    stdscr.getch()

# Initialize the curses application
curses.wrapper(main)
