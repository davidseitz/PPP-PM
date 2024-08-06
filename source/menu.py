"""
This module provides a command-line password manager using curses for the UI.

Functions:
- print_menu: Displays a menu in the terminal.
- get_input: Prompts the user for input.
- validateUser: Validates user login credentials.
- add_site_password: Adds a new password for a site.
- generate_password: Generates a random password based on user criteria.
- edit_password: Edits an existing password.
- delete_password: Deletes a password entry.
- find_password: Finds and displays a password for a site.
- view_all_sites: Display all entries in the terminal.
- password_manager: The password manager menu for a logged-in user.
- _terminalToSmall: Displays a message if the terminal is too small.
- main: The main function to run the password manager.
"""
import curses
import random
import string

from source import checkPwned
from source.checkPassword import checkDuplicate
from source.diskManagement import loadFromDisk, saveToDisk, loadEntryFromFile, exportToDisk

from .userManagement import saveUser, validateUser, userExists
from .entry import entry

def print_menu(stdscr, selected_row_idx, menu):
    """
    Displays a menu in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - selected_row_idx: Index of the currently selected row.
    - menu: List of menu items to display.
    """
    try:
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
    except curses.error:
        _terminalToSmall(stdscr)
def exportToFile(stdscr,username: str, userEntries: list) -> None:
    """
    Export the user's entries to a file.

    Parameters:
    - stdscr: The standard screen object from curses.
    - userEntries: A list of the users entries.
    """
    filepath = exportToDisk(username, userEntries)
    stdscr.clear()
    stdscr.addstr(1, 0, "Entries exported to file:")
    stdscr.addstr(2, 0, filepath)
    stdscr.addstr(3, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def _terminalToSmall(stdscr):
    try:
        stdscr.clear()
        stdscr.addstr(1, 0, "Please resize the terminal to be larger.")
        stdscr.addstr(2, 0, "Press any key to continue.")
        stdscr.refresh()
        stdscr.getch()
    except curses.error:
        with open("error.log", "w") as f:
            print("Please resize the terminal to be larger and restart the application.\n", file=f)
        exit(1)

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

def getInputLong(stdscr, prompt: str) -> str:
    """
    Prompts the user for input. That may be longer than the terminal width.
    """

    stdscr.clear()
    h, w = stdscr.getmaxyx()
    stdscr.addstr(h // 2 - 1, 0, prompt)
    stdscr.refresh()

    input_win = curses.newwin(1, w, h // 2, 0)
    curses.echo()  # Enable input echoing
    user_input = input_win.getstr().decode("utf-8")
    curses.noecho()  # Disable input echoing
    return user_input


def add_site_password(stdscr,username, userEntries):
    """
    Adds a new password for a site.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - userEntries: A list of the users entries.
    """
    site = get_input(stdscr, "Enter the name/web-URL/site you want to add: ")
    user = get_input(stdscr, "Enter the username: ")
    password = get_input(stdscr, "Enter the password: ")
    if get_input(stdscr, "Re-enter the password: ") != password:
        stdscr.clear()
        stdscr.addstr(1, 0, "Passwords do not match.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return
    if not evaluatePassword(stdscr, password, userEntries):
        return
    
    note = get_input(stdscr, "Enter any notes: ")
    
    e = entry(site, password, user, note)
    if not e in userEntries:
        userEntries.append(e)       
    else:
        stdscr.clear()
        stdscr.addstr(1, 0, f"Entry for website {site} already exists.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return
        
    stdscr.clear()
    if saveToDisk(username, userEntries):
        stdscr.addstr(1, 0, "Entry saved!")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.addstr(1, 0, "Failed to save entry.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
    
def evaluatePassword(stdscr, password: str, userEntries: list) -> bool:
    from .checkPassword import checkPassword
    if not checkPassword(password):
        stdscr.clear()
        stdscr.addstr(1, 0, "Password may be insecure.")
        stdscr.addstr(2, 0, "To ensure security, please use a password with at least 12 characters.")
        stdscr.addstr(3, 0, "Including uppercase and lowercase letters, digits, and special characters.")
        stdscr.addstr(4, 0, "Do you want to continue? (y/n)")
        answer: bool = False
        while True:
            key = stdscr.getch()
            if key == ord("y"):
                answer = True
                break
            elif key == ord("n"):
                answer = False
                break
        stdscr.refresh() 
        if not answer:
            return False
    try:
        wasPwned = checkPwned.checkPawned(password)
        if wasPwned:
            stdscr.clear()
            stdscr.addstr(1, 0, f"Password has been pawned {wasPwned} times.")
            stdscr.addstr(2, 0, "Do you want to continue anyway? (y/n)")
            answer: bool = False
            while True:
                key = stdscr.getch()
                if key == ord("y"):
                    answer = True
                    break
                elif key == ord("n"):
                    answer = False
                    break
            stdscr.refresh()
            if not answer:
                return  False  
    except checkPwned.RequestError as e:
        stdscr.clear()
        stdscr.addstr(1, 0, "Failed to check if password has been pawned.")
        stdscr.addstr(2, 0, f"API request failed: \"{e}\".")
        stdscr.addstr(3, 0, "Do you want to continue anyway? (y/n)")
        answer: bool = False
        while True:
            key = stdscr.getch()
            if key == ord("y"):
                answer = True
                break
            elif key == ord("n"):
                answer = False
                break
        stdscr.refresh()
        stdscr.getch()
        if not answer:
            return False
        
    if checkDuplicate(password, userEntries):
        stdscr.clear()
        stdscr.addstr(1, 0, "Password already exists.")
        stdscr.addstr(2, 0, "Do you want to continue anyway? (y/n)")
        answer: bool = False
        while True:
            key = stdscr.getch()
            if key == ord("y"):
                answer = True
                break
            elif key == ord("n"):
                answer = False
                break
        stdscr.refresh()
        if not answer:
            return False
    return True

def loadFromFile(stdscr, userEntries: list) -> list:
    """
    Load the user's entries from disk

    Parameters:
    - stdscr: The standard screen object from curses.

    Returns:
    - userEntries: A list of the users entries.
    """
    filepath = getInputLong(stdscr, "Enter the file path: ")
    try:
        userEntries = loadEntryFromFile(filepath, userEntries)
    except FileNotFoundError:
        stdscr.clear()
        stdscr.addstr(1, 0, "File not found.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
    except ValueError:
        stdscr.clear()
        stdscr.addstr(1, 0, "Invalid file format.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
    return userEntries

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
    stdscr.addstr(3, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def edit_password(stdscr, username: str, userEntries: list) -> None:
    """
    Edits an existing password.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - userEntries: A list of the users entries.
    """
    site = get_input(stdscr, "Enter the name/web-URL/site you want to edit: ")
    current_entry = None
    for entry in userEntries:
        if entry.website == site:
            current_entry = entry
            userEntries.remove(entry)
            break
    if current_entry is None:
        stdscr.clear()
        stdscr.addstr(1, 0, "Site not found.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return
    stdscr.clear()
    display_entry(stdscr, current_entry)
    stdscr.addstr(6, 0, "Is this the entry you want to edit? (y/n)")  
    answer: bool = False
    while True:
        key = stdscr.getch()
        if key == ord("y"):
            answer = True
            break
        elif key == ord("n"):
            answer = False
            break
    stdscr.refresh()
    stdscr.getch()
    if not answer:
        return
    stdscr.clear()
    stdscr.addstr(1, 0, "What do you want to edit? (use number to select and press Enter to confirm)")
    stdscr.addstr(2, 0, "1. Website")
    stdscr.addstr(3, 0, "2. Username")
    stdscr.addstr(4, 0, "3. Password")
    stdscr.addstr(5, 0, "4. Notes")
    stdscr.addstr(6, 0, "5. Cancel")
    stdscr.refresh()
    key = stdscr.getch()
    if key == ord("1"):
        new_site = get_input(stdscr, "Enter the new website: ")
        changeable = True
        for entry in userEntries:
            if entry.website == new_site:
                changeable = False
                break
        if changeable and current_entry.updateWebsite(new_site):
            stdscr.clear()
            stdscr.addstr(1, 0, "Website updated!")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
        else:
            stdscr.clear()
            stdscr.addstr(1, 0, "Website not updated. (Website already exists)")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
    elif key == ord("2"):
        new_username = get_input(stdscr, "Enter the new username: ")
        if current_entry.updateUsername(new_username):
            stdscr.clear()
            stdscr.addstr(1, 0, "Username updated!")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
        else:
            stdscr.clear()
            stdscr.addstr(1, 0, "Username not updated.")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
    elif key == ord("3"):
        new_password = get_input(stdscr, "Enter the new password: ")
        if current_entry.updatePassword(new_password):
            stdscr.clear()
            stdscr.addstr(1, 0, "Password updated!")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
        else:
            stdscr.clear()
            stdscr.addstr(1, 0, "Password not updated. You may not use an old password")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
    elif key == ord("4"):
        new_notes = get_input(stdscr, "Enter the new notes: ")
        if current_entry.updateNotes(new_notes):
            stdscr.clear()
            stdscr.addstr(1, 0, "Notes updated!")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
        else:
            stdscr.clear()
            stdscr.addstr(1, 0, "Notes not updated.")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
    elif key == ord("5"):
        userEntries.append(current_entry)
        return
    userEntries.append(current_entry)
    if saveToDisk(username, userEntries):
        pass    


def delete_password(stdscr, username: str, userEntries: list) -> None:
    """
    Deletes a password entry.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - userEntries: A list of the users entries.
    """
    
    site = get_input(stdscr, "Enter the name/web-URL/site you want to delete: ")
    for entry in userEntries:
        if entry.website == site:
            userEntries.remove(entry)
            stdscr.clear()
            stdscr.addstr(1, 0, "Entry deleted!")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
            if saveToDisk(username, userEntries):
                pass
            else:
                stdscr.clear()
                stdscr.addstr(1, 0, "Failed to delete entry.")
                stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
                stdscr.refresh()
                stdscr.getch()
            return
        
    stdscr.clear()
    stdscr.addstr(1, 0, "Entry not found.")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

    
def find_password(stdscr, userEntries):
    """
    Finds and displays a password for a site.

    Parameters:
    - stdscr: The standard screen object from curses.
    - userEntries: A list of the users entries.
    """
    menu = ["Find by URL", "Find by pattern"]
    current_row = 0
    while True:
        print_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord("\n"):
            break
    if current_row == 0:
        site = get_input(stdscr, "Enter the name/web-URL/site you want to find: ")
        from .findPasswords import findPasswordByUrl
        entry = findPasswordByUrl(userEntries, site)
        if entry is not None:
            if entry.website == site:
                stdscr.clear()
                stdscr.addstr(1, 0, f"Password for {site}: {entry.password}")
                stdscr.addstr(2, 0, f"Username: {entry.username}")
                stdscr.addstr(3, 0, f"Notes: {entry.notes}")
                stdscr.addstr(4, 0, "Press any key to return to the manager menu.")
                stdscr.refresh()
                stdscr.getch()
                return
    elif current_row == 1:
        pattern = get_input(stdscr, "Enter the pattern you want to find: ")
        from .findPasswords import findPasswordByPattern
        entries = findPasswordByPattern(userEntries, pattern)
        if len(entries) > 0:
            view_all_sites(stdscr, entries)
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
def display_entry(stdscr, entry: entry) -> None:
    """
    Display an entry in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - entry: The entry to display.
    """
    stdscr.clear()
    stdscr.addstr(1, 0, f"Website: {entry.website}")
    stdscr.addstr(2, 0, f"Username: {entry.username}")
    stdscr.addstr(3, 0, f"Password: {entry.password}")
    stdscr.addstr(4, 0, f"Notes: {entry.notes}")
    stdscr.addstr(5, 0, "-" * 50)

def view_all_sites(stdscr, userEntries: list) -> None:
    """
    Display all entries in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - userEntries: A list of the users entries.
    """
    stdscr.clear()
    for entry in userEntries:
        display_entry(stdscr, entry)
        if entry != userEntries[-1]:
            stdscr.addstr(6, 0, "Press any key to view the next entry.")
            stdscr.getch()
        else:
            break
    if len(userEntries) == 0:
        stdscr.clear()
        stdscr.addstr(1, 0, "No entries found.")
    stdscr.addstr(6, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def password_manager(stdscr, username: str):
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
        "View All Sites",
        "Load from File",
        "Export to File",
        "Logout",
    ]
    userEntries = loadFromDisk(username)

    while True:
        print_menu(stdscr, current_row, menu)
        key = stdscr.getch()
        if saveToDisk(username, userEntries):
            pass
        else:
            stdscr.clear()
            stdscr.addstr(1, 0, "Failed to save entries.")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(menu) - 1:
            current_row += 1
        elif key == ord("\n"):
            if current_row == 0:
                add_site_password(stdscr, username, userEntries)	
            elif current_row == 1:
                generate_password(stdscr)
            elif current_row == 2:
                edit_password(stdscr, username, userEntries)
            elif current_row == 3:
                delete_password(stdscr, username, userEntries)
            elif current_row == 4:
                find_password(stdscr, userEntries)
            elif current_row == 5:
                view_all_sites(stdscr, userEntries)
            elif current_row == 6:
                userEntries = loadFromFile(stdscr, userEntries)
            elif current_row == 7:
                exportToFile(stdscr, username, userEntries)
            elif current_row == 8:
                break


if __name__ == "__main__":
    curses.wrapper(main)
