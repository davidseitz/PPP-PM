"""
This file is used to run all the tests in the tests folder
"""
import unittest
from .testCheckPwned import TestHaveIBeenPwned

def testMain() -> None:
    """
    This function runs all the tests in the tests folder
    """

    suite = unittest.TestSuite()
    suite.addTest(TestHaveIBeenPwned('testHashPassword'))
    suite.addTest(TestHaveIBeenPwned('testCheckPawned'))

    runner = unittest.TextTestRunner()
    runner.run(suite)
