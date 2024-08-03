"""
This file is used to run all the tests in the tests folder
"""
import unittest
from .testCheckPwned import TestHaveIBeenPwned
from .testMenu import testMenu as TestMenu
from .testCheckPassword import TestCheckPassword

def testMain() -> None:
    """
    This function runs all the tests in the tests folder
    """

    suite = unittest.TestSuite()

    #HaveIBeenPwned tests
    suite.addTest(TestHaveIBeenPwned('testHashPassword'))
    suite.addTest(TestHaveIBeenPwned('testCheckPawned'))

    #Menu tests
    suite.addTest(TestMenu('test_save_user'))
    suite.addTest(TestMenu('test_validate_user_success'))
    suite.addTest(TestMenu('test_validate_user_fail'))
    suite.addTest(TestMenu('test_save_password_update'))
    suite.addTest(TestMenu('test_save_password_new'))

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
