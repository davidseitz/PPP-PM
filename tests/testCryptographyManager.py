"""
This file contains the tests for the cryptographyManager.py file.
"""
import unittest
import os

from source.cryptographyManager import encryptContent, decryptContent


class uTestCryptographyManager(unittest.TestCase):
    """
    This class contains the tests for the cryptographyManager.py file.
    """
    def testEncryptContent(self) -> None:
        self.assertTrue(encryptContent("test", "password", "username"))
        os.remove("resources/username_entries.enc")

    def testDecryptContent(self) -> None:
        """
        This method tests the decryptContent method of the cryptographyManager.py file.
        """
        self.assertTrue(encryptContent("test", "password", "username"))
        self.assertEqual(decryptContent("password", "username"), "test")
        os.remove("resources/username_entries.enc")

        self.assertTrue(encryptContent("", "password", "username"))
        self.assertEqual(decryptContent("password", "username"), "")
        os.remove("resources/username_entries.enc")

        self.assertEqual(decryptContent("password", "username"), "")
