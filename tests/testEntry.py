from contextlib import AbstractContextManager
from typing import Any
import unittest

from source.entry import entry

class TestEntry(unittest.TestCase):
    def testConstructor(self) -> None:
        entry1 = entry("testsite", "testpass", "testuser")
        self.assertEqual(entry1.username, "testuser")
        self.assertEqual(entry1.password, "testpass")
        self.assertEqual(entry1.website, "testsite")
        self.assertEqual(entry1.notes, "")
        self.assertEqual(entry1.oldPasswords, [])
        entry2 = entry("testsite", "testpass", "testuser", "testnotes", ["oldpass1", "oldpass2"])
        self.assertEqual(entry2.username, "testuser")
        self.assertEqual(entry2.password, "testpass")
        self.assertEqual(entry2.website, "testsite")
        self.assertEqual(entry2.notes, "testnotes")
        self.assertEqual(entry2.oldPasswords, ["oldpass1", "oldpass2"])
    
    def testUpdatePassword(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertTrue(entry1.updatePassword("newpass"))
        self.assertFalse(entry1.updatePassword("newpass"))
        self.assertFalse(entry1.updatePassword("testpass"))
        self.assertFalse(entry1.updatePassword("newpass"))
    
    def testUpdateUsername(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertTrue(entry1.updateUsername("newuser"))
        self.assertFalse(entry1.updateUsername("newuser"))
        self.assertTrue(entry1.updateUsername("testuser"))
    
    def testUpdateNotes(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertTrue(entry1.updateNotes("newnotes"))
        self.assertFalse(entry1.updateNotes("newnotes"))
        self.assertTrue(entry1.updateNotes("testnotes"))
    
    def testUpdateWebsite(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertTrue(entry1.updateWebsite("newsite"))
        self.assertFalse(entry1.updateWebsite("newsite"))
        self.assertTrue(entry1.updateWebsite("testsite"))
    
    def testStr(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertEqual(str(entry1), "testuser - testsite - testpass - ")

    def testEq(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        entry2 = entry("testuser", "testpass", "testsite")
        self.assertEqual(entry1, entry2)
        entry3 = entry("testuser", "testpass", "testsite", "testnotes", ["oldpass1", "oldpass2"])
        self.assertEqual(entry1, entry3)
        entry4 = entry("testuser2", "testpass", "testsite", "testnotes", ["oldpass1", "oldpass2"])
        self.assertNotEqual(entry1, entry4)
        self.assertNotEqual(entry3, entry4)