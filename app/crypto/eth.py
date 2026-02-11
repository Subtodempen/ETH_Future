import os
from eth_account import Account


class CryptoHandle:
    def __init__(self):
        self.private_key = None

    @property
    def private_key(self):
        if self._private_key is None:
            raise ValueError("Private Key not found")

        return self._private_key

    @private_key.setter
    def private_key(self, value):
        self._private_key = value

    def set_private_key(self):
        self.private_key = os.getenv("PRIVATE_KEY")

    def generate_address(self):
        return Account.from_key(self.private_key).address
        
    

