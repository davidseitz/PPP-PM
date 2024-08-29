""" This Model contains the entry class """
import time

class entry:
    """ This class represents an entry in the password manager """
    #suppressed the warning for the following method because [] is not equal to [""]
    #pylint: disable=W0102
    def __init__(self, website: str, password: str, username: str, timestmaps: list = [float(0)], notes: str = "", oldPasswords: list = [""]) -> None:
        self.website = website
        self.password = password
        self.username = username
        self.notes = notes
        self.oldPasswords = oldPasswords
        if timestmaps == [float(0)]:
            self.timestamps = [time.time()]
        else:
            self.timestamps = timestmaps

    def updatePassword(self, password: str) -> bool:
        """updates the password of the entry

        Args:
            password (str): the new password to update

        Returns:
            bool: True if the password was updated, False otherwise
        """
        if self.password == password:
            return False
        try:
            if password in self.oldPasswords:
                return False
        except TypeError:
            self.oldPasswords = []
        self.oldPasswords.append(self.password)
        self.oldPasswords.remove("")
        self.password = password
        self.timestamps.append(time.time())
        return True

    def updateUsername(self, username: str) -> bool:
        """
        Updates the username of the object.

        Args:
            username (str): The new username to be set.

        Returns:
            bool: True if the username was successfully updated, False otherwise.
        """
        if self.username == username:
            return False
        self.username = username
        self.timestamps.append(time.time())
        return True

    def updateNotes(self, notes: str) -> bool:
        """
        Updates the notes of the object.

        Args:
            notes (str): The new notes to be set.

        Returns:
            bool: True if the notes were successfully updated, False otherwise.
        """
        if self.notes == notes:
            return False
        self.notes = notes
        self.timestamps.append(time.time())
        return True

    def updateWebsite(self, website: str) -> bool:
        """
        Updates the website of the object.

        Args:
            website (str): The new website to be set.

        Returns:
            bool: True if the website was successfully updated, False otherwise.
        """
        if self.website == website:
            return False
        self.website = website
        self.timestamps.append(time.time())
        return True

    def getLastEditTime(self) -> str:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(self.timestamps[-1]))

    def __str__(self) -> str:
        return f"{self.website} - {self.username} - {self.password} - {self.notes}"

    #suppressed the warning for the following method because entry isn't initialized yet
    def __eq__(self, value) -> bool: # type: ignore
        return bool(self.website == value.website)
