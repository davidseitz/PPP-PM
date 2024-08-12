import pyotp
import qrcode
import os

class SecondFactor:
    def __init__(self, email: str):
        self.email = email
        
    def generateUrl(self, email: str)->str:
        return pyotp.totp.TOTP('JBSWY3DPEHPK3PXP').provisioning_uri(name=email, issuer_name='Password Manager')

    def generateQrCode(self, email: str)-> None:
        url = self.generateUrl(email)
        img = qrcode.make(url)
        img.save(os.getcwd() + '/qr.png')
    