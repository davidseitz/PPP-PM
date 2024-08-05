import json
import os
import time

from source.DiskManagement import getFilepath

MAX_ATTEMPTS = 3
LOCKOUT_TIME = 60  # 1 minute

def saveUser(username, password):
    """
    Saves user information to a JSON file.

    Parameters:
    - username: The username of the user.
    - password: The password of the user.
    """
    filename = f"{username}_user.json"
    userData = {
        "username": username,
        "password": password,
        "failed_attempts": 0,
        "lockout_time": 0,
    }

    with open(filename, "w", encoding="utf-8") as file:
        json.dump(userData, file, indent=4)
    path = getFilepath(username)
    with open(path, 'a'):
        os.utime(path, None)


def validateUser(username, password):
    """
    Validates user login credentials.

    Parameters:
    - username: The username of the user.
    - password: The password of the user.

    Returns:
    - A tuple containing a boolean indicating if the validation was successful and a message.
    """
    filename = f"{username}_user.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            user = json.load(file)
            current_time = time.time()

            if current_time < user.get("lockout_time", 0):
                return False, "Account locked due to multiple failed attempts. Try again later."

            if user["username"] == username and user["password"] == password:
                user["failed_attempts"] = 0
                user["lockout_time"] = 0
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(user, file, indent=4)
                return True, "Login successful."

            user["failed_attempts"] = user.get("failed_attempts", 0) + 1
            if user["failed_attempts"] >= MAX_ATTEMPTS:
                user["lockout_time"] = current_time + LOCKOUT_TIME
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(user, file, indent=4)
            return False, "Invalid username or password."

    return False, "Invalid username or password."


def userExists(username):
    """
    Checks if a user already exists.

    Parameters:
    - username: The username to check.

    Returns:
    - True if the user exists, False otherwise.
    """
    filename = f"{username}_user.json"
    return os.path.exists(filename)


def saveSitePassword(username :str, site :str, newPassword :str) -> bool:
    """
    Saves or updates a user's password for a site.

    Parameters:
    - username: The username of the user.
    - site: The site for which the password is being saved.
    - newPassword: The new password to save.

    Returns:
    - True if the password was saved successfully, False otherwise.
    """
    filename = f"{username}_passwords.json"
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as file:
            passwords = json.load(file)
    else:
        passwords = []
        return False # User does not exist

    for entry in passwords:
        if entry["site"] == site:
            if newPassword in entry.get("old_passwords", []):
                return False  # newPassword is an old password, don't save it
            entry["old_passwords"] = entry.get("old_passwords", []) + [entry["password"]]
            entry["password"] = newPassword
            break
    else:
        passwords.append({"site": site, "password": newPassword, "old_passwords": []})
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(passwords, file, indent=4)
    return True
