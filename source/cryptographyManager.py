"""this module is responsible for encrypting and decrypting the content of a file
"""
import os
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding

def decryptContent(password: str, username: str) -> str:
    """Decrypt the content of a file and returns it as a string

    Args:
        password (str): password to decrypt the content
        username (str): username for the file to decrypt

    Returns:
        str: decrypted content
    """
    # Read the encrypted content from the file
    filePath = f'resources/{username}_entries.enc'
    try:
        with open(filePath, 'rb') as file:
            encryptedContent = file.read()
    except FileNotFoundError:
        return ""

    # Extract the salt and IV from the encrypted content
    salt = encryptedContent[:16]
    initializationVector = encryptedContent[16:32]

    # Extract the actual encrypted data
    encryptedData = encryptedContent[32:]

    # Derive a key from the password using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Create an AES cipher with CBC mode
    try:
        cipher = Cipher(algorithms.AES(key), modes.CBC(initializationVector), backend=default_backend())
    except ValueError:
        return ""
    # Decrypt the encrypted data
    decryptor = cipher.decryptor()
    decryptedContent = decryptor.update(encryptedData)

    try:
        decryptedContent += decryptor.finalize()
    except ValueError:
        return ""

    # Create an unpadder with PKCS7 padding scheme
    unpadder = padding.PKCS7(128).unpadder()
    # Unpad the decrypted content
    try:
        unpaddedContent = unpadder.update(decryptedContent) + unpadder.finalize()
    except ValueError:
        return ""

    # Return the decrypted content
    return unpaddedContent.decode()

def encryptContent(content: str, password: str, username: str) -> bool:
    """Encrypts the content and writes it to a file

    Args:
        content (str): content to encrypt
        password (str): password to encrypt the content
        username (str): username for the file to encrypt

    Returns:
        bool: True if the file was written successfully, False otherwise
    """
    # Generate a salt for PBKDF2HMAC key derivation
    salt = os.urandom(16)

    # Derive a key from the password using PBKDF2HMAC
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
        backend=default_backend()
    )
    key = kdf.derive(password.encode())

    # Generate a random IV
    initializationVector = os.urandom(16)
    # Create an AES cipher with CBC mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(initializationVector), backend=default_backend())
    encryptor = cipher.encryptor()

    # Pad the content using PKCS7 padding scheme
    padder = padding.PKCS7(128).padder()
    paddedData = padder.update(content.encode()) + padder.finalize()

    # Encrypt the padded data
    encryptedContent = encryptor.update(paddedData) + encryptor.finalize()

    # Write the salt, IV, and encrypted content to the file
    filePath = f'resources/{username}_entries.enc'
    try:
        with open(filePath, 'wb') as file:
            file.write(salt + initializationVector + encryptedContent)
        return True
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    pass
