""" This class represents an entry in the password manager """

class entry:
    def __init__(self, website: str, password: str, username: str, notes: str = "", oldPasswords: list = []) -> None:
        self.website = website
        self.password = password
        self.username = username
        self.notes = notes
        self.oldPasswords = oldPasswords

    def updatePassword(self, password: str) -> bool:
        """updates the password of the entry

        Args:
            password (str): the new password to update

        Returns:
            bool: True if the password was updated, False otherwise
        """
        if self.password == password:
            return False
        if password in self.oldPasswords:
            return False
        self.oldPasswords.append(self.password)
        self.password = password
        return True

    def updateUsername(self, username: str) -> bool:
        if self.username == username:
            return False
        self.username = username
        return True

    def updateNotes(self, notes: str) -> bool:
        if self.notes == notes:
            return False
        self.notes = notes
        return True

    def updateWebsite(self, website: str) -> bool:
        if self.website == website:
            return False
        self.website = website
        return True

    def __str__(self) -> str:
        return f"{self.website} - {self.username} - {self.password} - {self.notes}"

    #suppressed the warning for the following method because it is a magic method
    #mypy: suppress = no-any-return
    def __eq__(self, value) -> bool:
        return bool(self.website == value.website)
