"""
This file is used to run all the tests in the tests folder
"""
import unittest

from testEntry import TestEntry
from testFindPasswords import TestFindPasswords
from testCheckPwned import TestHaveIBeenPwned
from testCheckPassword import TestCheckPassword
from testsUserManagement import TestUserManagement
from testDiskManagement import TestDiskManagement
from testCryptographyManager import TestCryptographyManager
from testSecondFactor import TestSecondFactor

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
    
    #Entry tests
    suite.addTest(TestEntry('testConstructor'))
    suite.addTest(TestEntry('testUpdatePassword'))
    suite.addTest(TestEntry('testUpdateUsername'))
    suite.addTest(TestEntry('testUpdateNotes'))
    suite.addTest(TestEntry('testUpdateWebsite'))
    suite.addTest(TestEntry('testStr'))
    suite.addTest(TestEntry('testEq'))

    #findPassword tests
    suite.addTest(TestFindPasswords('testFindPasswordByUrl'))
    suite.addTest(TestFindPasswords('testFindPasswordByPattern'))

    #DiskManagement tests
    suite.addTest(TestDiskManagement('testSaveToDisk'))
    suite.addTest(TestDiskManagement('testLoadFromDisk'))
    suite.addTest(TestDiskManagement('testGetFilepath'))
    suite.addTest(TestDiskManagement('testCreateFile'))
    suite.addTest(TestDiskManagement('testLoadEntryFromFile'))
    suite.addTest(TestDiskManagement('testExportToDisk'))

    #SecondFactor tests
    testSecondFactor = TestSecondFactor()
    suite.addTest(TestSecondFactor('testConstructor'))
    suite.addTest(TestSecondFactor('testGenerateQR'))
    suite.addTest(TestSecondFactor('testSecret'))
    suite.addTest(TestSecondFactor('testValidateCode'))
    suite.addTest(TestSecondFactor('testGenerateUrl'))
    
    #CryptographyManager tests
    suite.addTest(TestCryptographyManager('testEncryptContent'))
    suite.addTest(TestCryptographyManager('testDecryptContent'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
    testSecondFactor.tearDown()

if __name__ == "__main__":
    testMain()
