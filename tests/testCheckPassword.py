"""
This file contains the tests for the checkPassword.py file.
"""
import unittest
from source.checkPassword import checkPassword, _checkLength, _checkLowercase, \
    _checkUppercase, _checkDigit, _checkSpecial

class TestCheckPassword(unittest.TestCase):
    """
    This class contains the tests for the checkPassword.py file.
    """
    def testCheckPassword(self) -> None:
        self.assertTrue(checkPassword("Test1234!!@sadadad42311231."))
        self.assertFalse(checkPassword("Test1234"))
        self.assertFalse(checkPassword("test1234!!@sadadad42311231."))
        self.assertFalse(checkPassword("TEST1234!!@42311231."))
        self.assertFalse(checkPassword("Test!@sadadada"))
        

    def testCheckLength(self) -> None:
        self.assertTrue(_checkLength("Test1234!234"))
        self.assertTrue(_checkLength("Iam13characte"))
        self.assertFalse(_checkLength("Test1234"))

    def testCheckLowercase(self) -> None:
        self.assertTrue(_checkLowercase("Test1234!"))
        self.assertFalse(_checkLowercase("TEST1234!"))

    def testCheckUppercase(self) -> None:
        self.assertTrue(_checkUppercase("Test1234!"))
        self.assertFalse(_checkUppercase("test1234!"))

    def testCheckDigit(self) -> None:
        self.assertTrue(_checkDigit("Test1234!"))
        self.assertFalse(_checkDigit("Test!"))

    def testCheckSpecial(self) -> None:
        self.assertTrue(_checkSpecial("Test1234!"))
        self.assertFalse(_checkSpecial("Test1234"))
