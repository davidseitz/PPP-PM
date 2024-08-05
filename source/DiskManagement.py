import json
import os
from .entry import entry

def saveToDisk(user: str, userEntries: list) -> bool:
    """
    Save the user's entries to disk
    """
    filename = f"resources/{user}_entries.json"
    if os.path.exists(filename):
        with open(filename, "w") as file:
            json.dump([entry.__dict__ for entry in userEntries], file, indent=4)
        return True
    return False

def loadFromDisk(user: str) -> list:
    """
    Load the user's entries from disk
    """
    userEntries = []
    filename = f"resources/{user}_entries.json"
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                contents = json.load(file)
                for e in contents:
                    website = e["website"]
                    password = e["password"]
                    username = e["username"]
                    notes = e["notes"]
                    oldPasswords = e["oldPasswords"]
                    userEntries.append(entry(website, password, username, notes, oldPasswords))
            except json.JSONDecodeError:
                pass
    return userEntries

def createFile(user: str) -> bool:
    """
    Create a file for the user's entries
    """
    filename = f"resources/{user}_entries.json"
    if not os.path.exists(filename):
        os.touch(filename)
        return True
    return False

def loadEntryFromFile(filepath: str, userEntries: list) -> list:
    """
    Load an entry from a given file
    """
    with open(filepath, "r") as file:
        contents = json.load(file)
        contents = json.load(file)
        entry = entry(**contents)
        userEntries.append(entry)
    return userEntries

def getFilepath(user: str) -> str:
    """
    Get the filepath for the user's entries
    """
    return os.getcwd() + f"/resources/{user}_entries.json"
            