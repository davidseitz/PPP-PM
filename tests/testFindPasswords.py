"""
This file contains the tests for the findPasswords.py file.
"""
import unittest
from source.findPasswords import findPasswordByPattern, findPasswordByUrl
from source.entry import entry

class TestFindPasswords(unittest.TestCase):
    def testFindPasswordByUrl(self) -> None:
        entries = [entry("x", "a", "a", "a", [])]
        self.assertEqual(findPasswordByUrl(entries, "x"), entry("x", "a", "a", "a", []))
        self.assertEqual(findPasswordByUrl(entries, "y"), None)	
    
    def testFindPasswordByPattern(self) -> None:
        entries = [entry("x", "a", "a", "a", []), entry("y", "b", "b", "b", []), entry("z", "a", "c", "c", []), entry("w", "d", "a", "d", []), entry("v", "e", "e", "a", [])]
        self.assertEqual(findPasswordByPattern(entries, "a"), [entry("x", "a", "a", "a", []), entry("z", "a", "c", "c", []), entry("w", "d", "a", "d", []), entry("v", "e", "e", "a", [])])
        self.assertEqual(findPasswordByPattern(entries, "b"), [entry("y", "b", "b", "b", [])])
        self.assertEqual(findPasswordByPattern(entries, "k"), [])


