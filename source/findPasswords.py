from .entry import entry

def findPasswordByUrl(userEntries: list, url: str) -> entry:
    """
    Find the password for a given website
    """
    for e in userEntries:
        if e.website == url:
            return e
    return None

def findPasswordByPattern(userEntries: list, pattern: str) -> list:
    """
    Find the password for a given pattern
    """
    entries = []
    for e in userEntries:
        if pattern in e.website:
            entries.append(e)
        elif pattern in e.username:
            entries.append(e)
        elif pattern in e.notes:
            entries.append(e)
    return entries
