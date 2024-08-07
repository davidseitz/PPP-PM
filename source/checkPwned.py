"""
This script checks if a password has been pawned using the API from https://haveibeenpawned.com
"""

import hashlib
import requests

def checkPawned(password: str) -> int:
    """
    Check if a password has been pawned using the API from https://haveibeenpawned.com
    """
    password = hashPassword(password)
    url = 'https://api.pwnedpasswords.com/range/' + password[:5]
    try:
        response = requests.get(url, timeout=3)
    except requests.exceptions.RequestException as error:
        raise RuntimeError(f'Error fetching: {error}, check the API and try again')
    if response.status_code != 200:
        raise RuntimeError(f'Error fetching: {response.status_code}, check the API and try again')
    hashes = (line.split(':') for line in response.text.splitlines())
    for myHash, count in hashes:
        if myHash == password[5:]:
            return int(count)
    return 0

def hashPassword(password: str) -> str:
    """
    Hash the password using SHA1 algorithm
    """
    return hashlib.sha1(password.encode()).hexdigest().upper()
