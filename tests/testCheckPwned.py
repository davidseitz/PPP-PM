"""
This file contains the tests for the checkPwned.py file.
"""
import unittest
import requests

from source.checkPwned import checkPawned, hashPassword


class TestHaveIBeenPwned(unittest.TestCase):
    """
    This class contains the tests for the checkPwned.py file.
    """

    def testHashPassword(self) -> None:
        self.assertEqual(hashPassword("12345"), "8CB2237D0679CA88DB6464EAC60DA96345513964")

    def testCheckPawned(self) -> None:
        try:
            if requests.get("https://api.pwnedpasswords.com/range/8CB22").status_code != 200:
                self.skipTest("Pwned Passwords API is down")
            self.assertGreaterEqual(checkPawned("12345"), 1)
        except requests.exceptions.RequestException:
            self.skipTest("Connection is down")