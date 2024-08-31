"""
This module provides a command-line password manager using curses for the UI.

Functions:
- printMenu: Displays a menu in the terminal.
- getInput: Prompts the user for input.
- validateUser: Validates user login credentials.
- addSitePassword: Adds a new password for a site.
- generatePassword: Generates a random password based on user criteria.
- editPassword: Edits an existing password.
- deletePassword: Deletes a password entry.
- findPassword: Finds and displays a password for a site.
- viewAllSites: Display all entries in the terminal.
- passwordManager: The password manager menu for a logged-in user.
- _terminalToSmall: Displays a message if the terminal is too small.
- main: The main function to run the password manager.
- displayEntry: Display an entry in the terminal.
- exportToFile: Export the user's entries to a file.
- getInputLong: Prompts the user for input. That may be longer than the terminal width.
"""
import curses
import random
import string
import sys

from secondFactor import secondFactor as SecondFactor
from checkPwned import checkPawned
from checkPassword import checkDuplicate, checkPassword
from diskManagement import loadFromDisk, saveToDisk, loadEntryFromFile, exportToDisk
from userManagement import saveUser, validateUser, userExists
from entry import entry
from findPasswords import findPasswordByUrl, findPasswordByPattern


def printMenu(stdscr :curses.window, selectedRowIdx :int, menu :list) -> None:
    """
    Displays a menu in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - selectedRowIdx: Index of the currently selected row.
    - menu: List of menu items to display.
    """
    try:
        stdscr.clear()
        height, width = stdscr.getmaxyx()

        for idx, row in enumerate(menu):
            xCordinate = width // 2 - len(row) // 2
            yCordinate = height // 2 - len(menu) // 2 + idx
            if idx == selectedRowIdx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(yCordinate, xCordinate, row)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(yCordinate, xCordinate, row)
        stdscr.refresh()
    except curses.error:
        _terminalToSmall(stdscr)
def exportToFile(stdscr :curses.window,username: str, userEntries: list) -> None:
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


def _terminalToSmall(stdscr :curses.window) -> None:
    try:
        stdscr.clear()
        stdscr.addstr(1, 0, "Please resize the terminal to be larger.")
        stdscr.addstr(2, 0, "Press any key to continue.")
        stdscr.refresh()
        stdscr.getch()
    except curses.error:
        with open("error.log", "w", encoding="utf-8") as errorLog:
            print("Please resize the terminal to be larger and restart the application.\n", file=errorLog)
        sys.exit(1)

def getInput(stdscr :curses.window, prompt: str) -> str:
    """
    Prompts the user for input.

    Parameters:
    - stdscr: The standard screen object from curses.
    - prompt: The prompt message to display.

    Returns:
    - userInput: The input from the user as a string.
    """
    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height // 2 - 1, width // 2 - len(prompt) // 2, prompt)
    stdscr.refresh()

    inputWin = curses.newwin(1, len(prompt) + 10, height // 2, width // 2 - len(prompt) // 2)
    curses.echo()  # Enable input echoing
    userInput = inputWin.getstr().decode("utf-8")
    curses.noecho()  # Disable input echoing
    return userInput

def getInputLong(stdscr :curses.window, prompt: str) -> str:
    """
    Prompts the user for input. That may be longer than the terminal width.
    """

    stdscr.clear()
    height, width = stdscr.getmaxyx()
    stdscr.addstr(height // 2 - 1, 0, prompt)
    stdscr.refresh()

    inputWin = curses.newwin(1, width, height // 2, 0)
    curses.echo()  # Enable input echoing
    userInput = inputWin.getstr().decode("utf-8")
    curses.noecho()  # Disable input echoing
    return userInput


def addSitePassword(stdscr :curses.window, username: str, masterPassword: str, userEntries: list) -> None:
    """
    Adds a new password for a site.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - masterPassword: The masterPassword of the user.
    - userEntries: A list of the users entries.
    """
    site = getInput(stdscr, "Enter the name/web-URL/site you want to add: ")
    user = getInput(stdscr, "Enter the username: ")
    password = getInput(stdscr, "Enter the password: ")
    if getInput(stdscr, "Re-enter the password: ") != password:
        stdscr.clear()
        stdscr.addstr(1, 0, "Passwords do not match.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return
    if not evaluatePassword(stdscr, password, userEntries):
        return

    note = getInput(stdscr, "Enter any notes: ")

    newEntry = entry(site, password, user, notes=note)
    if not newEntry in userEntries:
        userEntries.append(newEntry)
    else:
        stdscr.clear()
        stdscr.addstr(1, 0, f"Entry for website {site} already exists.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return

    stdscr.clear()
    if saveToDisk(username, masterPassword, userEntries):
        stdscr.addstr(1, 0, "Entry saved!")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
    else:
        stdscr.addstr(1, 0, "Failed to save entry.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()

def evaluatePassword(stdscr :curses.window, password: str, userEntries: list) -> bool:
    """
    Evaluates the password for security.

    Parameters:
    - stdscr: The standard screen object from curses.
    - password: The password to evaluate.
    - userEntries: A list of the users entries.
    """
    if not checkPassword(password):
        stdscr.clear()
        stdscr.addstr(1, 0, "Password may be insecure.")
        stdscr.addstr(2, 0, "To ensure security, please use a password with at least 12 characters.")
        stdscr.addstr(3, 0, "Including uppercase and lowercase letters, digits, and special characters.")
        stdscr.addstr(4, 0, "Do you want to continue? (y/n)")
        answer: bool
        while True:
            key = stdscr.getch()
            if key == ord("y"):
                answer = True
                break
            if key == ord("n"):
                answer = False
                break
        stdscr.refresh()
        if not answer:
            return False
    try:
        wasPwned = checkPawned(password)
        if wasPwned:
            stdscr.clear()
            stdscr.addstr(1, 0, f"Password has been pawned {wasPwned} times.")
            stdscr.addstr(2, 0, "Do you want to continue anyway? (y/n)")
            answer3: bool = False
            while True:
                key = stdscr.getch()
                if key == ord("y"):
                    answer3 = True
                    break
                if key == ord("n"):
                    answer3 = False
                    break
            stdscr.refresh()
            if not answer3:
                return  False
    except RuntimeError as error:
        stdscr.clear()
        stdscr.addstr(1, 0, "Failed to check if password has been pawned.")
        stdscr.addstr(3, 0, f"API request failed: \"{error}\".")
        stdscr.addstr(2, 0, "Do you want to continue anyway? (y/n)")
        answer2: bool = False
        while True:
            key = stdscr.getch()
            if key == ord("y"):
                answer2 = True
                break
            if key == ord("n"):
                answer2 = False
                break
        stdscr.refresh()
        stdscr.getch()
        if not answer2:
            return False

    if checkDuplicate(password, userEntries):
        stdscr.clear()
        stdscr.addstr(1, 0, "Password already exists.")
        stdscr.addstr(2, 0, "Do you want to continue anyway? (y/n)")
        answer4: bool = False
        while True:
            key = stdscr.getch()
            if key == ord("y"):
                answer4 = True
                break
            if key == ord("n"):
                answer4 = False
                break
        stdscr.refresh()
        if not answer4:
            return False
    return True

def loadFromFile(stdscr :curses.window, username: str, password: str, userEntries: list) -> list:
    """
    Load the user's entries from disk

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - password: The password of the user.

    Returns:
    - userEntries: A list of the users entries.
    """
    filepath = getInputLong(stdscr, "Enter the file path: ")
    try:
        userEntries = loadEntryFromFile(filepath, userEntries)
        saveToDisk(username, password, userEntries)
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
    except TypeError:
        stdscr.clear()
        stdscr.addstr(1, 0, "Invalid file format.")
        stdscr.addstr(2, 0, "You shure you're files syntax looks like this?")
        example = """
        [
            {
                "website": "x",
                "password": "a",
                "username": "a",
                "notes": "a",
                "oldPasswords": []
            }
        ]
        """
        while True:
            try:
                for yCor, line in enumerate(example.splitlines(), 2):
                    stdscr.addstr(yCor, 2, line)
                break
            except curses.error:
                _terminalToSmall(stdscr)
        stdscr.refresh()
        stdscr.getch()
    return userEntries

def generatePassword(stdscr :curses.window) -> None:
    """
    Generates a random password based on user criteria.

    Parameters:
    - stdscr: The standard screen object from curses.
    """
    length: int
    while True:
        try:
            length = int(getInput(stdscr, "Enter password length: (number between 12 and 128)"))
            if 12 <= length <= 128:
                break
        except ValueError:
            pass

    optionsPassword = [
        "Include uppercase letters",
        "Include lowercase letters",
        "Include digits",
        "Include special characters",
    ]

    selectedOptions = [False] * len(optionsPassword)
    currentOptionIdx = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, "Select character types (press Space to choose and Enter to confirm):")
        for idx, option in enumerate(optionsPassword):
            if selectedOptions[idx]:
                optionText = "[X] " + option
            else:
                optionText = "[ ] " + option
            if idx == currentOptionIdx:
                stdscr.attron(curses.color_pair(1))
                stdscr.addstr(1 + idx, 0, optionText)
                stdscr.attroff(curses.color_pair(1))
            else:
                stdscr.addstr(1 + idx, 0, optionText)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and currentOptionIdx > 0:
            currentOptionIdx -= 1
        elif key == curses.KEY_DOWN and currentOptionIdx < len(optionsPassword) - 1:
            currentOptionIdx += 1
        elif key == ord(" "):
            selectedOptions[currentOptionIdx] = not selectedOptions[currentOptionIdx]
        elif key == ord("\n"):
            if any(selectedOptions):
                break

    characters = ""
    if selectedOptions[0]:  # Include uppercase letters
        characters += string.ascii_uppercase
    if selectedOptions[1]:  # Include lowercase letters
        characters += string.ascii_lowercase
    if selectedOptions[2]:  # Include digits
        characters += string.digits
    if selectedOptions[3]:  # Include special characters
        characters += string.punctuation

    password = "".join(random.choice(characters) for i in range(length))

    stdscr.clear()
    stdscr.addstr(1, 0, f"Generated password: {password}")
    stdscr.addstr(3, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()


def editPassword(stdscr :curses.window, username: str, password : str, userEntries: list) -> None:
    """
    Edits an existing password.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - password: The password of the user.
    - userEntries: A list of the users entries.
    """
    site = getInput(stdscr, "Enter the name/web-URL/site you want to edit: ")
    currentEntry = None
    for _entry in userEntries:
        if _entry.website == site:
            currentEntry = _entry
            userEntries.remove(_entry)
            break
    if currentEntry is None:
        stdscr.clear()
        stdscr.addstr(1, 0, "Site not found.")
        stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
        stdscr.refresh()
        stdscr.getch()
        return
    stdscr.clear()
    displayEntry(stdscr, currentEntry)
    stdscr.addstr(7, 0, "Is this the entry you want to edit? (y/n)")
    answer: bool = False
    while True:
        key = stdscr.getch()
        if key == ord("y"):
            answer = True
            break
        if key == ord("n"):
            answer = False
            break
    stdscr.refresh()
    if not answer:
        userEntries.append(currentEntry)
        if saveToDisk(username, password, userEntries):
            pass
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
        newSite = getInput(stdscr, "Enter the new website: ")
        changeable = True
        for _entry in userEntries:
            if _entry.website == newSite:
                changeable = False
                break
        if changeable and currentEntry.updateWebsite(newSite):
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
        newUsername = getInput(stdscr, "Enter the new username: ")
        if currentEntry.updateUsername(newUsername):
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
        newPassword = getInput(stdscr, "Enter the new password: ")
        if evaluatePassword(stdscr, newPassword, userEntries) and currentEntry.updatePassword(newPassword):
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
        newNotes = getInput(stdscr, "Enter the new notes: ")
        if currentEntry.updateNotes(newNotes):
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
        userEntries.append(currentEntry)
        return
    userEntries.append(currentEntry)
    if saveToDisk(username, password, userEntries):
        pass


def deletePassword(stdscr :curses.window, username: str, password : str, userEntries: list) -> None:
    """
    Deletes a password entry.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the user.
    - password: The password of the user.
    - userEntries: A list of the users entries.
    """

    site = getInput(stdscr, "Enter the name/web-URL/site you want to delete: ")
    for _entry in userEntries:
        if _entry.website == site:
            userEntries.remove(_entry)
            stdscr.clear()
            stdscr.addstr(1, 0, "Entry deleted!")
            stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            stdscr.refresh()
            stdscr.getch()
            if saveToDisk(username, password, userEntries):
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


def findPassword(stdscr :curses.window, userEntries: list) -> None:
    """
    Finds and displays a password for a site.

    Parameters:
    - stdscr: The standard screen object from curses.
    - userEntries: A list of the users entries.
    """
    menu = ["Find by URL", "Find by pattern"]
    currentRow = 0
    while True:
        printMenu(stdscr, currentRow, menu)
        key = stdscr.getch()
        if key == curses.KEY_UP and currentRow > 0:
            currentRow -= 1
        elif key == curses.KEY_DOWN and currentRow < len(menu) - 1:
            currentRow += 1
        elif key == ord("\n"):
            break
    if currentRow == 0:
        site = getInput(stdscr, "Enter the name/web-URL/site you want to find: ")
        _entry = findPasswordByUrl(userEntries, site)
        if _entry is not None:
            if _entry.website == site:
                stdscr.clear()
                stdscr.addstr(1, 0, f"Password for {site}: {_entry.password}")
                stdscr.addstr(2, 0, f"Username: {_entry.username}")
                stdscr.addstr(3, 0, f"Notes: {_entry.notes}")
                stdscr.addstr(4, 0, "Press any key to return to the manager menu.")
                stdscr.refresh()
                stdscr.getch()
                return
    elif currentRow == 1:
        pattern = getInput(stdscr, "Enter the pattern you want to find: ")
        entries = findPasswordByPattern(userEntries, pattern)
        if len(entries) > 0:
            viewAllSites(stdscr, entries)
            return

    stdscr.clear()
    stdscr.addstr(1, 0, "Password not found.")
    stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def activate2FA(stdscr: curses.window, username: str) -> None:
    """
    Activate 2FA for the user.

    Parameters:
    - stdscr: The standard screen object from curses.
    """
    stdscr.clear()
    stdscr.addstr(1,0, "You need an authentication app like google authenticator to activate 2FA")
    stdscr.addstr(3,0, "Please enter you're E-mail address:")
    userMail = getInput(stdscr, "Enter the E-mail address: ")
    secondFactorObject = SecondFactor(username)
    qrFile = secondFactorObject.generateQrCode(userMail)
    stdscr.clear()
    stdscr.addstr(1, 0, "QR-Code generated at:")
    stdscr.addstr(2, 0, f"{qrFile}")
    stdscr.addstr(3, 0, "Please scan this QR-Code with your authentication app. (e.g. Authenticator)")
    stdscr.addstr(4, 0, "2FA is now activated.")
    stdscr.addstr(5, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()
    stdscr.clear()


def options(stdscr: curses.window, username: str) -> None:
    """
    Display the options menu.

    Parameters:
    - stdscr: The standard screen object from curses.
    """
    menu = ["Activate 2FA",
            "Return to Manager Menu"]
    currentRow = 0
    while True:
        printMenu(stdscr, currentRow, menu)
        key = stdscr.getch()
        if key == curses.KEY_UP and currentRow > 0:
            currentRow -= 1
        elif key == curses.KEY_DOWN and currentRow < len(menu) - 1:
            currentRow += 1
        elif key == ord("\n"):
            break
    if currentRow == 0:
        activate2FA(stdscr, username)
    elif currentRow == 1:
        return

def main(stdscr: curses.window) -> None:
    """
    The main function to run the password manager.

    Parameters:
    - stdscr: The standard screen object from curses.
    """
    stdscr = curses.initscr()
    curses.curs_set(0)
    curses.start_color()
    curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)

    currentRow = 0

    menu = ["Login", "Register", "Exit"]

    while True:
        printMenu(stdscr, currentRow, menu)
        key = stdscr.getch()

        if key == curses.KEY_UP and currentRow > 0:
            currentRow -= 1
        elif key == curses.KEY_DOWN and currentRow < len(menu) - 1:
            currentRow += 1
        elif key == ord("\n"):
            if currentRow == 0:
                username = getInput(stdscr, "Enter username: ")
                masterPassword = getInput(stdscr, "Enter password: ")
                valid, message = validateUser(username, masterPassword)
                stdscr.clear()
                stdscr.addstr(1, 0, message)
                stdscr.refresh()
                stdscr.getch()
                if message == "2FA required.": # Überprüfen
                    stdscr.clear()
                    stdscr.addstr(1, 0, "2FA required.")
                    stdscr.addstr(2, 0, "Please enter the code from your authentication app:")
                    code = getInput(stdscr, "Please enter the code from your authentication app: ")
                    if SecondFactor(username).validateCode(code):
                        valid = True
                    else:
                        stdscr.clear()
                        stdscr.addstr(1, 0, "Invalid code.")
                        stdscr.addstr(2, 0, "Are you're clocks synced?")
                        stdscr.addstr(3, 0, "Press any key to return to the Login menu.")
                        stdscr.refresh()
                        stdscr.getch()
                if valid:
                    passwordManager(stdscr, username, masterPassword)
            elif currentRow == 1:
                username = getInput(stdscr, "Enter username: ")
                if userExists(username):
                    stdscr.clear()
                    stdscr.addstr(1, 0, "Username already exists.")
                    stdscr.refresh()
                    stdscr.getch()
                else:
                    newMasterPassword = getInput(stdscr, "Enter password: ")
                    saveUser(username, newMasterPassword)
                    stdscr.clear()
                    stdscr.addstr(1, 0, "User registered successfully.")
                    stdscr.refresh()
                    stdscr.getch()
            elif currentRow == 2:
                break


def displayEntry(stdscr: curses.window, entryO: entry) -> None:
    """
    Display an entry in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - entryO: The entry to display.
    """
    stdscr.clear()
    stdscr.addstr(1, 0, f"Website: {entryO.website}")
    stdscr.addstr(2, 0, f"Username: {entryO.username}")
    stdscr.addstr(3, 0, f"Password: {entryO.password}")
    stdscr.addstr(4, 0, f"Notes: {entryO.notes}")
    stdscr.addstr(5, 0, f"Last changed: {entryO.getLastEditTime()}")
    stdscr.addstr(6, 0, "-" * 50)

def viewAllSites(stdscr :curses.window, userEntries: list) -> None:
    """
    Display all entries in the terminal.

    Parameters:
    - stdscr: The standard screen object from curses.
    - userEntries: A list of the users entries.
    """
    stdscr.clear()
    for _entry in userEntries:
        displayEntry(stdscr, _entry)
        if _entry != userEntries[-1]:
            stdscr.addstr(7, 0, "Press any key to view the next entry.")
            stdscr.getch()
        else:
            break
    if len(userEntries) == 0:
        stdscr.clear()
        stdscr.addstr(1, 0, "No entries found.")
    stdscr.addstr(7, 0, "Press any key to return to the manager menu.")
    stdscr.refresh()
    stdscr.getch()

def passwordManager(stdscr :curses.window, username: str, masterPassword: str) -> None:
    """
    The password manager menu for a logged-in user.

    Parameters:
    - stdscr: The standard screen object from curses.
    - username: The username of the logged-in user.
    - masterPassword: The masterPassword of the logged-in user.
    """
    currentRow = 0

    menu = [
        "Add Password",
        "Generate Password",
        "Edit Password",
        "Delete Password",
        "Find Password",
        "View All Sites",
        "Load from File",
        "Export to File",
        "Options",
        "Logout",
    ]
    userEntries = loadFromDisk(username, masterPassword)
    while True:
        printMenu(stdscr, currentRow, menu)
        key = stdscr.getch()
        # Unneccessary? and courses problems with encryption
        #if saveToDisk(username, password, userEntries):
            #pass
        #else:
            #stdscr.clear()
            #stdscr.addstr(1, 0, "Failed to save entries.")
            #stdscr.addstr(2, 0, "Press any key to return to the manager menu.")
            #stdscr.refresh()
            #stdscr.getch()
        if key == curses.KEY_UP and currentRow > 0:
            currentRow -= 1
        elif key == curses.KEY_DOWN and currentRow < len(menu) - 1:
            currentRow += 1
        elif key == ord("\n"):
            match currentRow:
                case 0:
                    addSitePassword(stdscr, username, masterPassword, userEntries)
                case 1:
                    generatePassword(stdscr)
                case 2:
                    editPassword(stdscr, username, masterPassword, userEntries)
                case 3:
                    deletePassword(stdscr, username, masterPassword, userEntries)
                case 4:
                    findPassword(stdscr, userEntries)
                case 5:
                    viewAllSites(stdscr, userEntries)
                case 6:
                    userEntries = loadFromFile(stdscr,username, masterPassword, userEntries)
                case 7:
                    exportToFile(stdscr, username, userEntries)
                case 8:
                    options(stdscr, username)
                case 9:
                    break


if __name__ == "__main__":
    curses.wrapper(main)
