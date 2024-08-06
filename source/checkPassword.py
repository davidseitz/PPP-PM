from checkPwned import checkPawned

def checkPassword(password: str) -> bool:
    """
    Check if a password is strong enough
    """
    if not _checkLength(password):
        return False
    if not _checkLowercase(password):
        return False
    if not _checkUppercase(password):
        return False
    if not _checkDigit(password):
        return False
    if not _checkSpecial(password):
        return False
    return True

def _checkLength(password: str) -> bool:
    """
    Check if a password is at least 12 characters long
    """
    return len(password) >= 12

def _checkLowercase(password: str) -> bool:
    """
    Check if a password has at least one lowercase letter
    """
    return any(char.islower() for char in password)

def _checkUppercase(password: str) -> bool:
    """
    Check if a password has at least one uppercase letter
    """
    return any(char.isupper() for char in password)

def _checkDigit(password: str) -> bool:
    """
    Check if a password has at least one digit
    """
    return any(char.isdigit() for char in password)

def _checkSpecial(password: str) -> bool:
    """
    Check if a password has at least one special character
    """
    return any(not char.isalnum() for char in password)
    
def checkDuplicate(password: str, userEntries: list) -> bool:
    """
    Check if a password has been used before
    """
    passwords = []
    for entry in userEntries:
        passwords.append(entry.password)
        passwords.extend(entry.oldPasswords)
    return password in passwords 