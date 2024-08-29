"""
This file contains the unit tests for the userManagement module.
"""
import unittest
import os

from source.userManagement import saveUser, validateUser, userExists

class uTestUserManagement(unittest.TestCase):
    """
    This class contains the tests for the userManagement module.
    """

    def testSaveUser(self) -> None:
        saveUser("test_user", "test_password")
        self.assertTrue(userExists("test_user"))
        self.assertFalse(userExists("wrong_user"))

    def testValidateUser(self) -> None:
        """
        This method tests the validateUser method of the userManagement module.
        """
        validated, message = validateUser("test_user", "test_password")
        self.assertTrue(validated)
        self.assertEqual(message, "Login successful.")
        validated, message = validateUser("test_user", "wrong_password")
        self.assertFalse(validated)
        self.assertEqual(message, "Invalid username or password.")
        validated, message = validateUser("wrong_user", "test_password")
        self.assertFalse(validated)
        self.assertEqual(message, "Invalid username or password.")
        validated, message = validateUser("test_user", "wrong_password")
        validated, message = validateUser("test_user", "wrong_password")
        validated, message = validateUser("test_user", "wrong_password")
        self.assertFalse(validated)
        self.assertEqual(message, "Account locked due to multiple failed attempts. Try again later.")

    def testUserExists(self) -> None:
        self.assertTrue(userExists("test_user"))
        self.assertFalse(userExists("wrong_user"))
        os.remove(f"{os.getcwd()}/resources/test_user_user.json")
