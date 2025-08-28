# crypto_utils.py
from cryptography.fernet import Fernet

class CryptoManager:
    def __init__(self, key: bytes = None):
        if key is None:
            self.key = Fernet.generate_key()
        else:
            self.key = key
        self.fernet = Fernet(self.key)

    def encrypt(self, message: bytes) -> bytes:
        return self.fernet.encrypt(message)

    def decrypt(self, token: bytes) -> bytes:
        return self.fernet.decrypt(token)

    def get_key(self) -> bytes:
        return self.key
