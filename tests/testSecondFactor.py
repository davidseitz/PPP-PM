"""
This file contains the tests for the secondFactor.py file.
"""
import unittest
import os
# pylint: disable=E0401
# Ignore the error because that was done in SecondFactor.py
import pyotp

from source.userManagement import saveUser
from source.secondFactor import secondFactor as SecondFactor

# pylint: disable=W0212
# Ignore access to a protected member of a client because this is a test file


class uTestSecondFactor(unittest.TestCase):
    """
    This class contains the tests for the secondFactor.py file.
    """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        saveUser("test_user", "test_password")

    def testConstructor(self) -> None:
        """
        This method tests the constructor of the secondFactor class.
        """
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        secondFactor2 = SecondFactor("test_user")
        self.assertEqual(secondFactor.username, "test_user")
        self.assertEqual(secondFactor.secret, secondFactor2.secret)
        self.assertEqual(secondFactor.username, secondFactor2.username)

    def testGenerateQR(self) -> None:
        """
        This method tests the generateQrCode method of the secondFactor class.
        """
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        self.assertEqual(secondFactor.secret,"")
        self.assertEqual(f"{os.getcwd()}/resources/qr.png", secondFactor.generateQrCode("mail"))
        self.assertNotEqual(secondFactor.secret, "")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/resources/qr.png"))
        


    def testSecret(self) -> None:
        """
        This method tests the _secret method of the secondFactor class.
        """
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        self.assertEqual(len(secondFactor._secret()), 32)
        self.assertNotEqual(secondFactor._secret(), secondFactor._secret())

    def testValidateCode(self) -> None:
        """
        This method tests the validateCode method of the secondFactor class.
        """
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        secondFactor.secret = secondFactor._secret()
        self.assertTrue(secondFactor.validateCode(pyotp.totp.TOTP(secondFactor.secret).now()))
        self.assertFalse(secondFactor.validateCode("123456"))

    def testGenerateUrl(self) -> None:
        """
        This method tests the generateUrl method of the secondFactor class.
        """
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        secondFactor.secret = "1234567890"
        secondFactor.email = "a@mail.de"
        temp = pyotp.totp.TOTP(secondFactor.secret).provisioning_uri(name=secondFactor.email, issuer_name='Password Manager')
        self.assertEqual(secondFactor.generateUrl(), temp)

    def tearDown(self) -> None:
        """
        This method cleans up the files created during the tests.
        """
        try:
            os.remove(f"{os.getcwd()}/resources/test_user_user.json")
            os.remove(f"{os.getcwd()}/resources/test_user_entries.enc")
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{os.getcwd()}/resources/qr.png")
        except FileNotFoundError:
            pass
