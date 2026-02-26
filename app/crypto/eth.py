from bip_utils import Bip39MnemonicGenerator, Bip39SeedGenerator, Bip39WordsNum, Bip44, Bip44Changes, Bip44Coins
import os

class CryptoHandle:
    def __init__(self, mnemonic, index = 0):
        self.mnemonic = mnemonic    
        self.index = index
        self.bip44_chg_ctx = None
        self.bip44_mstr_ctx = None

        self.construct_bip_acc()
        
    @classmethod
    def from_env(cls, index = 0):
        mnemonic = os.getenv("MNEMONIC")

        if not mnemonic:
            raise ValueError("Could not load mnemonic from dotenv")

        return cls(mnemonic, index)
    
    def construct_bip_acc(self):
        # generate Seed from mnemonic
        # create the master bip44 object
        # Configure the path
        seed_bytes = Bip39SeedGenerator(self.mnemonic).Generate()
        self.bip44_mstr_ctx = Bip44.FromSeed(seed_bytes, Bip44Coins.ETHEREUM)

        bip44_acc_ctx = self.bip44_mstr_ctx.Purpose().Coin().Account(0)
        self.bip44_chg_ctx = bip44_acc_ctx.Change(Bip44Changes.CHAIN_EXT)

    def get_bip44_index(self):
        return self.index

    # Gets in a user index not the current one
    def generate_account_from_index(self, index):
        return self.bip44_chg_ctx.AddressIndex(index)
    
    def generate_new_address(self):
        account = self.generate_account_from_index(self.index)
        address = account.PublicKey().ToAddress()

        self.index += 1
        return address
    
