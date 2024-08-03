"""
This file contains the tests for the checkPwned.py file.
"""
import unittest
from source.checkPwned import checkPawned, hashPassword


class TestHaveIBeenPwned(unittest.TestCase):
    """
    This class contains the tests for the checkPwned.py file.
    """

    def testHashPassword(self) -> None:
        self.assertEqual(hashPassword("12345"), "8CB2237D0679CA88DB6464EAC60DA96345513964")

    def testCheckPawned(self) -> None:
        self.assertGreaterEqual(checkPawned("12345"), 1)
