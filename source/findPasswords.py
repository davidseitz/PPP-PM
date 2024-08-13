""" This module contains functions to find passwords in the user's password manager """
from entry import entry

def findPasswordByUrl(userEntries: list, url: str) -> entry|None:
    """
    Find the password for a given website
    """
    userEntry: entry
    for userEntry in userEntries:
        if userEntry.website == url:
            return userEntry
    return None

def findPasswordByPattern(userEntries: list, pattern: str) -> list:
    """
    Find the password for a given pattern
    """
    entries = []
    for userEntry in userEntries:
        if pattern in userEntry.website:
            entries.append(userEntry)
        elif pattern in userEntry.username:
            entries.append(userEntry)
        elif pattern in userEntry.notes:
            entries.append(userEntry)
        elif pattern in userEntry.password:
            entries.append(userEntry)
    return entries
