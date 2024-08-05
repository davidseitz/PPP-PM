import unittest
import os

from source.diskManagement import saveToDisk, loadFromDisk, getFilepath, loadEntryFromFile, createFile 

class TestDiskManagement(unittest.TestCase):
    def testGetFilepath(self) -> None:
        self.assertEqual(getFilepath("test_user"), os.getcwd()+ "/resources/test_user_entries.json")
    
    def testCreateFile(self) -> None:
        os.remove(getFilepath("test_user"))
        self.assertTrue(createFile("test_user"))
        self.assertFalse(createFile("test_user"))
        self.assertTrue(os.path.exists(getFilepath("test_user")))
        os.remove(getFilepath("test_user"))

    def testSaveToDisk(self) -> None:
        createFile("test_user1")
        self.assertTrue(saveToDisk("test_user1", []))
        self.assertFalse(saveToDisk("test_user2", []))
        os.remove(getFilepath("test_user1"))

    def testLoadFromDisk(self) -> None:
        createFile("test_user1")
        self.assertEqual(loadFromDisk("test_user1"), [])
        os.remove(getFilepath("test_user1"))

    def testLoadEntryFromFile(self) -> None:
        #TODO: Implement this test
        pass