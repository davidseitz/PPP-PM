"""
This file contains the tests for the findPasswords.py file.
"""
import unittest
from source.findPasswords import findPasswordByPattern, findPasswordByUrl
from source.entry import entry

class uTestFindPasswords(unittest.TestCase):
    """
    This class contains the tests for the findPasswords.py file.
    """

    def testFindPasswordByUrl(self) -> None:
        entries = [entry("x", "a", "a", [float(4)], "a", [])]
        self.assertEqual(findPasswordByUrl(entries, "x"), entry("x", "a", "a", [float(4)], "a", []))
        self.assertEqual(findPasswordByUrl(entries, "y"), None)

    def testFindPasswordByPattern(self) -> None:
        """
        This method tests the findPasswordByPattern method of the findPasswords.py file.
        """
        entries = [entry("x", "a", "a",[float(4)], "a", []), entry("y", "b", "b",[float(4)], "b", []),
                    entry("z", "a", "c",[float(4)], "c", []), entry("w", "d", "a",[float(4)] , "d", []), entry("v", "e", "e", [float(4)], "a", [])]
        self.assertEqual(findPasswordByPattern(entries, "a"),[entry("x", "a", "a", [float(4)], "a", []),
                                                              entry("z", "a", "c", [float(4)], "c", []), entry("w", "d", "a", [float(4)], "d", []),
                                                                entry("v", "e", "e", [float(4)], "a", [])])
        self.assertEqual(findPasswordByPattern(entries, "b"), [entry("y", "b", "b", [float(4)], "b", [])])
        self.assertEqual(findPasswordByPattern(entries, "k"), [])
