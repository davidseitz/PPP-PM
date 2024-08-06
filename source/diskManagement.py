import json
import os
from source.entry import entry
from source.cryptographyManager import decryptContent, encryptContent

def saveToDisk(user: str, password :str, userEntries: list) -> bool:
    """
    Save the user's entries to disk
    """
    filename = f"resources/{user}_entries.enc"
    if os.path.exists(filename):
        return encryptContent(str([entry.__dict__ for entry in userEntries]), password, user)
    return False

def loadFromDisk(user: str, password : str) -> list:
    """
    Load the user's entries from disk
    """
    userEntries = []
    filename = f"resources/{user}_entries.enc"
    if os.path.exists(filename):
        try:
            decrypted_entries = decryptContent(password,user)
            contents = json.loads(decrypted_entries.replace("'", "\""))
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
    filename = getFilepath(user)
    if os.path.exists(filename):
        return False
    with open(filename, 'a'):
        os.utime(filename, None)
    return True

def loadEntryFromFile(filepath: str, userEntries: list) -> list:
    """
    Load an entry from a given file
    This method is not ready for serial use
    """
    with open(filepath, "r") as file:
        contents = json.load(file)
    try:
        for e in contents:
            website = e["website"]
            password = e["password"]
            username = e["username"]
            notes = e["notes"]
            oldPasswords = e["oldPasswords"]
            userEntries.append(entry(website, password, username, notes, oldPasswords))
    except json.JSONDecodeError:
        raise ValueError("Invalid file format") 
    return userEntries

def getFilepath(user: str) -> str:
    """
    Get the filepath for the user's entries
    """
    return os.getcwd() + f"/resources/{user}_entries.enc"

def exportToDisk(user: str, userEntries: list) -> str:
    """
    Export the user's entries to disk
    """
    filename = os.getcwd() + f"/{user}_exports.json"
    with open(filename, "w") as file:
        json.dump([entry.__dict__ for entry in userEntries], file, indent=4)
    return filename

            