""" This module contains functions for managing user information. """
import json
import os
import time
import hashlib

from source.diskManagement import getFilepath

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
    hashedPassword = hashlib.sha256(password.encode()).hexdigest()
    userData = {
        "username": username,
        "password": hashedPassword,
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
            currentTime = time.time()

            if currentTime < user.get("lockout_time", 0):
                return False, "Account locked due to multiple failed attempts. Try again later."

            hashedPassword = hashlib.sha256(password.encode()).hexdigest()
            if user["username"] == username and user["password"] == hashedPassword:
                user["failed_attempts"] = 0
                user["lockout_time"] = 0
                with open(filename, "w", encoding="utf-8") as file:
                    json.dump(user, file, indent=4)
                return True, "Login successful."

            user["failed_attempts"] = user.get("failed_attempts", 0) + 1
            if user["failed_attempts"] >= MAX_ATTEMPTS:
                user["lockout_time"] = currentTime + LOCKOUT_TIME
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
