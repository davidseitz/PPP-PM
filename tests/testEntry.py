import unittest
import time
from source.entry import entry

class TestEntry(unittest.TestCase):
    def testConstructor(self) -> None:
        entry1 = entry("testsite", "testpass", "testuser")
        self.assertEqual(entry1.username, "testuser")
        self.assertEqual(entry1.password, "testpass")
        self.assertEqual(entry1.website, "testsite")
        self.assertEqual(entry1.notes, "")
        self.assertEqual(entry1.oldPasswords, [""])
        self.assertLessEqual(entry1.timestamps[0], time.time())
        self.assertEqual(len(entry1.timestamps), 1)
        self.assertAlmostEqual(entry1.timestamps[0], time.time(), delta=1)
        entry2 = entry("testsite", "testpass", "testuser", [float(1)], "testnotes", ["oldpass1", "oldpass2"])
        self.assertEqual(entry2.username, "testuser")
        self.assertEqual(entry2.password, "testpass")
        self.assertEqual(entry2.website, "testsite")
        self.assertEqual(entry2.notes, "testnotes")
        self.assertEqual(entry2.oldPasswords, ["oldpass1", "oldpass2"])
        self.assertEqual(entry2.timestamps[0], float(1))
    
    def testUpdatePassword(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        time1 = time.time()
        self.assertTrue(entry1.updatePassword("newpass"))
        self.assertFalse(entry1.updatePassword("newpass"))
        self.assertFalse(entry1.updatePassword("testpass"))
        self.assertFalse(entry1.updatePassword("newpass"))
        self.assertEqual(entry1.oldPasswords, ["testpass"])
        self.assertEqual(entry1.password, "newpass")
        self.assertGreater(entry1.timestamps[1], time1)


    
    def testUpdateUsername(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        time1 = time.time()
        self.assertTrue(entry1.updateUsername("newuser"))
        self.assertFalse(entry1.updateUsername("newuser"))
        self.assertTrue(entry1.updateUsername("testuser"))
        self.assertGreater(entry1.timestamps[1], time1)

    
    def testUpdateNotes(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        time1 = time.time()
        self.assertTrue(entry1.updateNotes("newnotes"))
        self.assertFalse(entry1.updateNotes("newnotes"))
        self.assertTrue(entry1.updateNotes("testnotes"))
        self.assertGreater(entry1.timestamps[1], time1)
    
    def testUpdateWebsite(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        time1 = time.time()
        self.assertTrue(entry1.updateWebsite("newsite"))
        self.assertFalse(entry1.updateWebsite("newsite"))
        self.assertTrue(entry1.updateWebsite("testsite"))
        self.assertGreater(entry1.timestamps[1], time1)
    
    def testStr(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertEqual(str(entry1), "testuser - testsite - testpass - ")

    def testEq(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        entry2 = entry("testuser", "testpass", "testsite")
        self.assertEqual(entry1, entry2)
        entry3 = entry("testuser", "testpass", "testsite",[float(3)], "testnotes", ["oldpass1", "oldpass2"])
        self.assertEqual(entry1, entry3)
        entry4 = entry("testuser2", "testpass", "testsite",[float(3)], "testnotes", ["oldpass1", "oldpass2"])
        self.assertNotEqual(entry1, entry4)
        self.assertNotEqual(entry3, entry4)

    def testGetLastEditTime(self) -> None:
        entry1 = entry("testuser", "testpass", "testsite")
        self.assertEqual(entry1.getLastEditTime(), time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(entry1.timestamps[-1])))