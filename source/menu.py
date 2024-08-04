"""
This module provides a command-line password manager using curses for the UI.

Functions:
- print_menu: Displays a menu in the terminal.
- get_input: Prompts the user for input.
- validateUser: Validates user login credentials.
- add_password: Adds a new password for a site.
- generate_password: Generates a random password based on user criteria.
- edit_password: Edits an existing password.
- delete_password: Deletes a password entry.
- find_password: Finds and displays a password for a site.
- main: The main function to run the password manager.
"""
import curses
import json
import os
import random
import string

from .userManagement import saveUser, validateUser, userExists, savePassword


def print_menu(stdscr, selected_row_idx, menu):
    """
    Displays a menu in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - selected_row_idx: Index of the currently selected row.
    - menu: List of menu items to display.
    """
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
    """
    Prompts the user for input.

    Parameters:
    - stdscr: The standard screen object from curses.
    - prompt: The prompt message to display.

    Returns:
    - user_input: The input from the user as a string.
    """
    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, w // 2 - len(prompt) // 2, prompt)
    stdscr.refresh()

    input_win = curses.newwin(1, len(prompt) + 10, h // 2, w // 2 - len(prompt) // 2)
    curses.echo()  # Enable input echoing
    user_input = input_win.getstr().decode("utf-8")
    curses.noecho()  # Disable input echoing
    return user_input



def add_password(stdscr, username):
    """
    Adds a new password for a site.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    """
    site = get_input(stdscr, "Enter the name/web-URL/site you want to add: ")
    password = get_input(stdscr, "Enter the password: ")

    if not savePassword(username, site, password):
        stdscr.clear()
        stdscr.addstr(1, 0, "Password cannot be one of the old passwords.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    stdscr.addstr(1, 0, "Password saved!")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def generate_password(stdscr):
    """
    Generates a random password based on user criteria.

    Parameters:
    - stdscr: The standard screen object from curses.
    """
    length = int(get_input(stdscr, "Enter password length: "))

    options = [
        "Include uppercase letters",
        "Include lowercase letters",
        "Include digits",
        "Include special characters",
    ]

    selected_options = [False] * len(options)
    current_option_idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select character types (press Space to choose and Enter to confirm):")
        for idx, option in enumerate(options):
            if selected_options[idx]:
                option_text = "[X] " + option
            else:
                option_text = "[ ] " + option
            if idx == current_option_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(1 + idx, 0, option_text)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(1 + idx, 0, option_text)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_option_idx > 0:
            current_option_idx -= 1
        elif key == curses.KEY_DOWN and current_option_idx < len(options) - 1:
            current_option_idx += 1
        elif key == ord(" "):
            selected_options[current_option_idx] = not selected_options[current_option_idx]
        elif key == ord("\n"):
            if any(selected_options):
                break

    characters = ""
    if selected_options[0]:  # Include uppercase letters
        characters += string.ascii_uppercase
    if selected_options[1]:  # Include lowercase letters
        characters += string.ascii_lowercase
    if selected_options[2]:  # Include digits
        characters += string.digits
    if selected_options[3]:  # Include special characters
        characters += string.punctuation

    password = "".join(random.choice(characters) for i in range(length))

    stdscr.clear()
    stdscr.addstr(1, 0, f"Generated password: {password}")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def edit_password(stdscr, username):
    """
    Edits an existing password.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    """
    filename = f"{username}_passwords.json"

    if not os.path.exists(filename):
        stdscr.clear()
        stdscr.addstr(1, 0, "No passwords found.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, "r", encoding="utf-8") as file:
        passwords = json.load(file)

    sites = [entry["site"] for entry in passwords]

    current_site_idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select a site to edit its password (use arrow keys and press Enter to select):")
        for idx, site in enumerate(sites):
            if idx == current_site_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(1 + idx, 0, site)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(1 + idx, 0, site)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_site_idx > 0:
            current_site_idx -= 1
        elif key == curses.KEY_DOWN and current_site_idx < len(sites) - 1:
            current_site_idx += 1
        elif key == ord("\n"):
            break

    new_password = get_input(stdscr, f"Enter the new password for {sites[current_site_idx]}: ")

    if not savePassword(username, sites[current_site_idx], new_password):
        stdscr.clear()
        stdscr.addstr(1, 0, "Password cannot be one of the old passwords.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    stdscr.addstr(1, 0, "Password updated!")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def delete_password(stdscr, username):
    """
    Deletes a password entry.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    """
    filename = f"{username}_passwords.json"

    if not os.path.exists(filename):
        stdscr.clear()
        stdscr.addstr(1, 0, "No passwords found.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, "r", encoding="utf-8") as file:
        passwords = json.load(file)

    sites = [entry["site"] for entry in passwords]

    current_site_idx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select a site to delete its password (use arrow keys and press Enter to select):")
        for idx, site in enumerate(sites):
            if idx == current_site_idx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(1 + idx, 0, site)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(1 + idx, 0, site)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_site_idx > 0:
            current_site_idx -= 1
        elif key == curses.KEY_DOWN and current_site_idx < len(sites) - 1:
            current_site_idx += 1
        elif key == ord("\n"):
            break

    passwords = [entry for entry in passwords if entry["site"] != sites[current_site_idx]]

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(passwords, file, indent=4)

    stdscr.clear()
    stdscr.addstr(1, 0, "Password deleted!")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def find_password(stdscr, username):
    """
    Finds and displays a password for a site.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    """
    site = get_input(stdscr, "Enter the name/web-URL/site you want to find: ")
    filename = f"{username}_passwords.json"

    if not os.path.exists(filename):
        stdscr.clear()
        stdscr.addstr(1, 0, "No passwords found.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    with open(filename, "r", encoding="utf-8") as file:
        passwords = json.load(file)

    for entry in passwords:
        if entry["site"] == site:
            stdscr.clear()
            stdscr.addstr(1, 0, f"Password for {site}: {entry['password']}")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
            return

    stdscr.clear()
    stdscr.addstr(1, 0, "Password not found.")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def main(stdscr):
    """
    The main function to run the password manager.

    Parameters:
    - stdscr: The standard screen object from curses.
    """
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row = 0

    menu = ["Login", "Register", "Exit"]

    while True:
        print_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord("\n"):
            if current_row == 0:
                username = get_input(stdscr, "Enter username: ")
                password = get_input(stdscr, "Enter password: ")
                valid, message = validateUser(username, password)
                stdscr.clear()
                stdscr.addstr(1, 0, message)
                stdscr.refresh()
                stdscr.getch()
                if valid:
                    password_manager(stdscr, username)
            elif current_row == 1:
                username = get_input(stdscr, "Enter username: ")
                if userExists(username):
                    stdscr.clear()
                    stdscr.addstr(1, 0, "Username already exists.")
                    stdscr.refresh()
                    stdscr.getch()
                else:
                    password = get_input(stdscr, "Enter password: ")
                    saveUser(username, password)
                    stdscr.clear()
                    stdscr.addstr(1, 0, "User registered successfully.")
                    stdscr.refresh()
                    stdscr.getch()
            elif current_row == 2:
                break


def password_manager(stdscr, username):
    """
    The password manager menu for a logged-in user.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the logged-in user.
    """
    current_row = 0

    menu = [
        "Add Password",
        "Generate Password",
        "Edit Password",
        "Delete Password",
        "Find Password",
        "Logout",
    ]

    while True:
        print_menu(stdscr, current_row, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord("\n"):
            if current_row == 0:
                add_password(stdscr, username)
            elif current_row == 1:
                generate_password(stdscr)
            elif current_row == 2:
                edit_password(stdscr, username)
            elif current_row == 3:
                delete_password(stdscr, username)
            elif current_row == 4:
                find_password(stdscr, username)
            elif current_row == 5:
                break


if __name__ == "__main__":
    curses.wrapper(main)
