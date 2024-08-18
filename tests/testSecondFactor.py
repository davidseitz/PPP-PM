from source.secondFactor import secondFactor as SecondFactor
import unittest
import os
import pyotp
from source.userManagement import saveUser

class TestSecondFactor(unittest.TestCase):
    """
    This class contains the tests for the secondFactor.py file.
    """
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        saveUser("test_user", "test_password")

    def testConstructor(self) -> None:
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        secondFactor2 = SecondFactor("test_user")
        self.assertEqual(secondFactor.username, "test_user")
        self.assertEqual(secondFactor.secret, secondFactor2.secret)
        self.assertEqual(secondFactor.username, secondFactor2.username)
    
    def testGenerateQR(self) -> None:
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        self.assertEqual(secondFactor.secret,"")
        self.assertEqual(secondFactor.generateQrCode("mail"), None)
        self.assertNotEqual(secondFactor.secret, "")
        self.assertTrue(os.path.exists(f"{os.getcwd()}/resources/qr.png"))

    def testSecret(self) -> None:
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        self.assertEqual(len(secondFactor._secret()), 32)
        self.assertNotEqual(secondFactor._secret(), secondFactor._secret())

    def testValidateCode(self) -> None:
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        secondFactor.secret = secondFactor._secret()
        self.assertFalse(secondFactor.validateCode("123456"))

    def testGenerateUrl(self) -> None:
        saveUser("test_user", "test_password")
        secondFactor = SecondFactor("test_user")
        secondFactor.secret = "1234567890"	
        secondFactor.email = "a@mail.de"
        self.assertEqual(secondFactor.generateUrl(), pyotp.totp.TOTP(secondFactor.secret).provisioning_uri(name=secondFactor.email, issuer_name='Password Manager'))
        
    def tearDown(self) -> None:
        try:
            os.remove(f"{os.getcwd()}/resources/test_user_user.json")
            os.remove(f"{os.getcwd()}/resources/test_user_entries.enc")
        except FileNotFoundError:
            pass
        try:
            os.remove(f"{os.getcwd()}/resources/qr.png")
        except FileNotFoundError:
            pass