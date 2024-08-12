import pyotp
import qrcode
import os

class SecondFactor:
    """
    Class to generate a QR code for the user to scan and enable 2FA

    Methods
    -------
    generateUrl(email: str)->str
        Returns the URL to generate the QR code
    generateQrCode(email: str)-> None
        Generates the QR code and saves it to the current directory
    """
    def __init__(self, email: str):
        self.email = email
        
    def generateUrl(self)->str:
        return pyotp.totp.TOTP('JBSWY3DPEHPK3PXP').provisioning_uri(name=self.email, issuer_name='Password Manager')

    def generateQrCode(self)-> None:
        url = self.generateUrl()
        img = qrcode.make(url)
        img.save(os.getcwd() + '/qr.png')
    