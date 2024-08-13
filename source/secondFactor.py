""" This Module contains the class to handel second factor auth"""

import json
import os
#pylint: disable=import-error
import pyotp
#Ignore untyped third party library
import qrcode #type: ignore

class secondFactor:
    """
    Class to generate a QR code for the user to scan and enable 2FA

    Methods
    -------
    generateUrl(email: str)->str
        Returns the URL to generate the QR code
    generateQrCode(email: str)-> None
        Generates the QR code and saves it to the current directory
    """
    def __init__(self, username: str)-> None:
        self.username = username
        filename = os.getcwd() + f"/resources/{username}_user.json"
        with open(filename, "r", encoding="utf-8") as file:
            user = json.load(file)
            self.email = user["2fa_mail"]
            self.secret = user["2fa_secret"]

    def generateUrl(self)->str:
        return pyotp.totp.TOTP(self.secret).provisioning_uri(name=self.email, issuer_name='Password Manager')

    def generateQrCode(self, email: str)-> None:
        """
        This method generates a QR code for the user to scan and enable 2FA
        """
        self.secret = self._secret()
        self.email = email
        filename = os.getcwd() + f"/resources/{self.username}_user.json"
        with open(filename, "r", encoding="utf-8") as file:
            user = json.load(file)
            user["2fa_enabled"] = True
            user["2fa_secret"] = self.secret
            user["2fa_mail"] = self.email
            with open(filename, "w", encoding="utf-8") as file:
                json.dump(user, file, indent=4)
        url = self.generateUrl()
        img = qrcode.make(url)
        img.save(os.getcwd() + '/qr.png')

    def validateCode(self, code: str)-> bool:
        totp = pyotp.TOTP(self.secret)
        return totp.verify(code)
    # pylint: disable=C0303
    # C0303: Trailing whitespace disabled because it looks nicer this way
    # pylint: disable=R0201
    # R0201: Method could be a function disabled because it needs to be a method
    # pylint: enable=C0303
    def _secret(self)->str:
        return pyotp.random_base32()
    