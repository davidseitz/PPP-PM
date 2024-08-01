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

def save_password(username, site, new_password):
    filename = f"{username}_passwords.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            passwords = json.load(file)
    else:
        passwords = []

    for entry in passwords:
        if entry["site"] == site:
            if new_password in entry.get("old_passwords", []):
                return False  # new_password is an old password, don't save it
            entry["old_passwords"] = entry.get("old_passwords", []) + [entry["password"]]
            entry["password"] = new_password
            break
    else:
        passwords.append({
            "site": site,
            "password": new_password,
            "old_passwords": []
        })

    with open(filename, "w") as file:
        json.dump(passwords, file, indent=4)
    
    return True

def add_password(stdscr, username):
    site = get_input(stdscr, "Enter the name/web-URL/site you want to add: ")
    password = get_input(stdscr, "Enter the password: ")

    if not save_password(username, site, password):
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
    # Generate a random password
    length = int(get_input(stdscr, "Enter password length: "))
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(random.choice(characters) for i in range(length))

    stdscr.clear()
    stdscr.addstr(1, 0, f"Generated Password: {password}")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def edit_password(stdscr, username, site):
    new_password = get_input(stdscr, "Enter the new password: ")

    if not save_password(username, site, new_password):
        stdscr.clear()
        stdscr.addstr(1, 0, "New password cannot be one of the old passwords.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    stdscr.addstr(1, 0, "Password updated!")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def delete_password(stdscr, username, site):
    filename = f"{username}_passwords.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            passwords = json.load(file)
        
        passwords = [entry for entry in passwords if entry["site"] != site]

        with open(filename, "w") as file:
            json.dump(passwords, file, indent=4)

    stdscr.clear()
    stdscr.addstr(1, 0, "Password deleted!")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def find_password(stdscr, username):
    site = get_input(stdscr, "Enter the name/web-URL/site to find: ")
    filename = f"{username}_passwords.json"

    if os.path.exists(filename):
        with open(filename, "r") as file:
            passwords = json.load(file)
            for entry in passwords:
                if entry["site"] == site:
                    stdscr.clear()
                    stdscr.addstr(1, 0, f"Password for {site}: {entry['password']}")
                    stdscr.addstr(2, 0, "Press any key to continue.")
                    stdscr.refresh()
                    stdscr.getch()
                    
                    sub_menu = ["Edit password", "Delete password", "Back to manager menu"]
                    current_row_idx = 0

                    while True:
                        print_menu(stdscr, current_row_idx, sub_menu)
                        key = stdscr.getch()

                        if key == curses.KEY_UP and current_row_idx > 0:
                            current_row_idx -= 1
                        elif key == curses.KEY_DOWN and current_row_idx < len(sub_menu) - 1:
                            current_row_idx += 1
                        elif key == ord('\n'):
                            selected_option = sub_menu[current_row_idx]
                            if selected_option == "Back to manager menu":
                                return
                            elif selected_option == "Edit password":
                                edit_password(stdscr, username, site)
                            elif selected_option == "Delete password":
                                delete_password(stdscr, username, site)
                            break
                    return
    stdscr.clear()
    stdscr.addstr(1, 0, f"No password found for {site}.")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def main(stdscr):
    curses.curs_set(0)
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    current_row_idx = 0
    main_menu = ["Login", "Register", "Exit"]

    while True:
        print_menu(stdscr, current_row_idx, main_menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and current_row_idx > 0:
            current_row_idx -= 1
        elif key == curses.KEY_DOWN and current_row_idx < len(main_menu) - 1:
            current_row_idx += 1
        elif key == ord('\n'):
            selected_option = main_menu[current_row_idx]

            if selected_option == "Exit":
                break
            elif selected_option == "Login":
                username = get_input(stdscr, "Enter username: ")
                password = get_input(stdscr, "Enter password: ")

                if validate_user(username, password):
                    manager_menu = ["Add password", "Find password", "Generate password", "Logout"]
                    current_manager_idx = 0

                    while True:
                        print_menu(stdscr, current_manager_idx, manager_menu)
                        key = stdscr.getch()

                        if key == curses.KEY_UP and current_manager_idx > 0:
                            current_manager_idx -= 1
                        elif key == curses.KEY_DOWN and current_manager_idx < len(manager_menu) - 1:
                            current_manager_idx += 1
                        elif key == ord('\n'):
                            manager_option = manager_menu[current_manager_idx]

                            if manager_option == "Logout":
                                break
                            elif manager_option == "Add password":
                                add_password(stdscr, username)
                            elif manager_option == "Find password":
                                find_password(stdscr, username)
                            elif manager_option == "Generate password":
                                generate_password(stdscr)
                else:
                    stdscr.clear()
                    stdscr.addstr(1, 0, "Invalid username or password.")
                    stdscr.addstr(2, 0, "Press any key to return to the main menu.")
                    stdscr.refresh()
                    stdscr.getch()
            elif selected_option == "Register":
                username = get_input(stdscr, "Enter new username: ")
                password = get_input(stdscr, "Enter new password: ")

                save_user(username, password)

                stdscr.clear()
                stdscr.addstr(1, 0, "User registered successfully!")
                stdscr.addstr(2, 0, "Press any key to return to the main menu.")
                stdscr.refresh()
                stdscr.getch()

curses.wrapper(main)


