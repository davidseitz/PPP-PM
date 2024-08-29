"""
This file contains the tests for the diskManagement module.
"""
import unittest
import os
from source.entry import entry
from source.diskManagement import saveToDisk, loadFromDisk, getFilepath, loadEntryFromFile, createFile, exportToDisk

class uTestDiskManagement(unittest.TestCase):
    """
    This class contains the tests for the diskManagement module.
    """

    def testGetFilepath(self) -> None:
        self.assertEqual(getFilepath("test_user"), os.getcwd()+ "/resources/test_user_entries.enc")

    def testCreateFile(self) -> None:
        """
        This method tests the createFile method of the diskManagement module.
        """
        os.remove(getFilepath("test_user"))
        self.assertTrue(createFile("test_user"))
        self.assertFalse(createFile("test_user"))
        self.assertTrue(os.path.exists(getFilepath("test_user")))
        os.remove(getFilepath("test_user"))

    def testSaveToDisk(self) -> None:
        """
        This method tests the saveToDisk method of the diskManagement module.
        """
        createFile("test_user1")
        self.assertTrue(saveToDisk("test_user1","user1_password", []))
        self.assertFalse(saveToDisk("test_user2","user1_password", []))
        os.remove(getFilepath("test_user1"))

    def testLoadFromDisk(self) -> None:
        """
        This method tests the loadFromDisk method of the diskManagement module.
        """
        createFile("test_user1")
        self.assertEqual(loadFromDisk("test_user1","user1_password"), [])
        os.remove(getFilepath("test_user1"))

    def testLoadEntryFromFile(self) -> None:
        """
        This method tests the loadEntryFromFile method of the diskManagement module.
        """
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
        with open("test.json", "w", encoding="utf-8") as file:
            file.write(contents)
        self.assertEqual(loadEntryFromFile("test.json", []),[entry("x", "a", "a", notes="a", oldPasswords=[])])
        os.remove("test.json")

    def testExportToDisk(self) -> None:
        self.assertEqual(exportToDisk("test_user", []), os.getcwd()+ "/resources/test_user_exports.json")
        os.remove(os.getcwd()+ "/resources/test_user_exports.json")
