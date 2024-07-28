import curses
import json
import os
import random
import string

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

def validate_user(username, password):
    if os.path.exists("user.json"):
        with open("user.json", "r") as file:
            users = json.load(file)
            for user in users:
                if user["username"] == username and user["password"] == password:
                    return True
    return False

def save_password(username, site, password):
    filename = f"{username}_passwords.json"
    password_data = {
        "site": site,
        "password": password
    }

    if os.path.exists(filename):
        with open(filename, "r") as file:
            passwords = json.load(file)
    else:
        passwords = []

    passwords.append(password_data)

    with open(filename, "w") as file:
        json.dump(passwords, file, indent=4)

def add_password(stdscr, username):
    site = get_input(stdscr, "Enter the name/web-URL/site you want to add: ")
    password = get_input(stdscr, "Enter the password: ")

    save_password(username, site, password)

    stdscr.clear()
    stdscr.addstr(1, 0, "Password saved!")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def generate_password(stdscr):
    # Generate a random password
    length = int(get_input(stdscr, "Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))

    stdscr.clear()
    stdscr.addstr(1, 0, f"Generated Password: {password}")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def manager_menu(stdscr, username):
    menu = ["Add password", "Find password", "Edit password", "Generate password", "Back to main menu"]
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
            if selected_option == "Back to main menu":
                break
            elif selected_option == "Add password":
                add_password(stdscr, username)
            elif selected_option == "Generate password":
                generate_password(stdscr)
            else:
                stdscr.clear()
                stdscr.addstr(0, 0, f"You selected '{selected_option}'.")
                stdscr.addstr(1, 0, "This feature is not implemented yet.")
                stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
                stdscr.refresh()
                stdscr.getch()
        print_menu(stdscr, current_row_idx, menu)

def login(stdscr):
#    get_input(stdscr, "Please log in using your username and password. Press any key to continue.")
    username = get_input(stdscr, "Enter username: ")
    password = get_input(stdscr, "Enter password: ")

    if validate_user(username, password):
        stdscr.clear()
        stdscr.addstr(1, 0, "Login successful!")
        stdscr.refresh()
        stdscr.getch()
        manager_menu(stdscr, username)
    else:
        stdscr.clear()
        stdscr.addstr(1, 0, "Invalid username or password.")
        stdscr.addstr(3, 0, "Press any key to return to the menu.")
        stdscr.refresh()
        stdscr.getch()

def register(stdscr):
#    get_input(stdscr, "Please add a username and a password. Press any key to continue.")
    username = get_input(stdscr, "Enter your new username: ")
    password = get_input(stdscr, "Enter your new password: ")

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
