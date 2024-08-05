class entry:
    def __init__(self, website: str, password: str, username: str, notes: str = "", oldPasswords: list = []) -> None:	
        self.website = website
        self.password = password
        self.username = username
        self.notes = notes
        self.oldPasswords = oldPasswords
    
    def updatePassword(self, password: str) -> bool:
        if self.password == password:
            return False
        elif password in self.oldPasswords:
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
    
    def __eq__(self, value: object) -> bool:
        return self.website == value.website
