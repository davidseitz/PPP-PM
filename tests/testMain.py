"""
This file is used to run all the tests in the tests folder
"""
import unittest

from tests.testEntry import TestEntry
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

    #CheckPassword tests
    suite.addTest(TestCheckPassword('testCheckPassword'))
    suite.addTest(TestCheckPassword('testCheckLength')) 
    suite.addTest(TestCheckPassword('testCheckLowercase'))
    suite.addTest(TestCheckPassword('testCheckUppercase'))
    suite.addTest(TestCheckPassword('testCheckDigit'))
    suite.addTest(TestCheckPassword('testCheckSpecial'))
    suite.addTest(TestCheckPassword('testCheckPwned'))

    #Entry tests
    suite.addTest(TestEntry('testConstructor'))
    suite.addTest(TestEntry('testUpdatePassword'))
    suite.addTest(TestEntry('testUpdateUsername'))
    suite.addTest(TestEntry('testUpdateNotes'))
    suite.addTest(TestEntry('testUpdateWebsite'))
    suite.addTest(TestEntry('testStr'))
    suite.addTest(TestEntry('testEq'))


    runner = unittest.TextTestRunner()
    runner.run(suite)
