"""
This file contains the tests for the cryptographyManager.py file.
"""
import unittest
import os

from source.cryptographyManager import encryptContent, decryptContent


class TestCryptographyManager(unittest.TestCase):
    def testEncryptContent(self) -> None:
        self.assertTrue(encryptContent("test", "password", "username"))
        os.remove("resources/username_entries.enc")
    
    def testDecryptContent(self) -> None:
        self.assertTrue(encryptContent("test", "password", "username"))
        self.assertEqual(decryptContent("password", "username"), "test")
        os.remove("resources/username_entries.enc")