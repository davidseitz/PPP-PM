"""
This file is used to run all the tests in the tests folder
"""
import unittest
from .testCheckPwned import TestHaveIBeenPwned
from .testCheckPassword import TestCheckPassword
from .testsUserManagement import TestUserManagement

def testMain() -> None:
    """
    This function runs all the tests in the tests folder
    """

    suite = unittest.TestSuite()

    #HaveIBeenPwned tests
    suite.addTest(TestHaveIBeenPwned('testHashPassword'))
    suite.addTest(TestHaveIBeenPwned('testCheckPawned'))

    #Menu tests
    #suite.addTest(TestMenu('test_save_password_update'))
    #suite.addTest(TestMenu('test_save_password_new'))

    #UserManagement tests
    suite.addTest(TestUserManagement('testSaveUser'))
    suite.addTest(TestUserManagement('testValidateUser'))
    suite.addTest(TestUserManagement('testUserExists'))
    suite.addTest(TestUserManagement('testSavePassword'))

    #CheckPassword tests
    suite.addTest(TestCheckPassword('testCheckPassword'))
    suite.addTest(TestCheckPassword('testCheckLength')) 
    suite.addTest(TestCheckPassword('testCheckLowercase'))
    suite.addTest(TestCheckPassword('testCheckUppercase'))
    suite.addTest(TestCheckPassword('testCheckDigit'))
    suite.addTest(TestCheckPassword('testCheckSpecial'))
    suite.addTest(TestCheckPassword('testCheckPwned'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
