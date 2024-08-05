import unittest
import os
from source.entry import entry
from source.diskManagement import saveToDisk, loadFromDisk, getFilepath, loadEntryFromFile, createFile, exportToDisk 

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
        contents = """
        [
            {
                "website": "x",
                "password": "a",
                "username": "a",
                "notes": "a",
                "oldPasswords": []
            }
        ]
        """
        with open("test.json", "w") as file:
            file.write(contents)  
        self.assertEqual(loadEntryFromFile("test.json", []), [entry("x", "a", "a", "a", [])]) 
        os.remove("test.json")

    def testExportToDisk(self) -> None:
        self.assertEqual(exportToDisk("test_user", []), os.getcwd()+ "/test_user_exports.json")
        os.remove(os.getcwd()+ "/test_user_exports.json")