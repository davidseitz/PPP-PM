"""
This file is used to run all the tests in the tests folder
"""
import unittest

from testEntry import uTestEntry as TestEntry
from testFindPasswords import uTestFindPasswords as TestFindPasswords
from testCheckPwned import uTestHaveIBeenPwned as TestHaveIBeenPwned
from testCheckPassword import uTestCheckPassword as TestCheckPassword
from testsUserManagement import uTestUserManagement as TestUserManagement
from testDiskManagement import uTestDiskManagement as TestDiskManagement
from testCryptographyManager import uTestCryptographyManager as TestCryptographyManager
from testSecondFactor import uTestSecondFactor as TestSecondFactor
#from tests.testMenuPrototype.testMenu import testMenu

def testMain() -> None:
    """
    This function runs all the tests in the tests folder
    """

    suite = unittest.TestSuite()

    #HaveIBeenPwned tests
    suite.addTest(TestHaveIBeenPwned('testHashPassword'))
    suite.addTest(TestHaveIBeenPwned('testCheckPawned'))

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
    suite.addTest(TestEntry('testGetLastEditTime'))

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
