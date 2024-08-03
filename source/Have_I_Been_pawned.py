import requests
import hashlib

def check_pawned(password: str) -> int:
    password = hash_password(password)
    url = 'https://api.pwnedpasswords.com/range/' + password[:5]
    response = requests.get(url)
    hashes = (line.split(':') for line in response.text.splitlines())
    for h, count in hashes:
        if h == password[5:]:
            return count
    return 0

def hash_password(password: str) -> str:

    return hashlib.sha1(password.encode()).hexdigest()

if __name__ == '__main__':
    password = "12345"
    count = check_pawned(password)
    if count:
        print(f"Password {password} has been found {count} times")
    else:
        print(f"Password {password} has not been found")