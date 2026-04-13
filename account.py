from dataclasses import dataclass, field
from typing import List
from keypair import KeyPair
from signature import Signature
from hash_util import sha256_str

@dataclass
class Account:
    account_id: str
    wallet: List[KeyPair] = field(default_factory=list)
    balance: int = 0

    @staticmethod
    def gen_account():
        kp = KeyPair.gen_keypair()
        account_id = sha256_str(kp.public_key)[:16]
        return Account(account_id=account_id, wallet=[kp], balance=0)

    def add_keypair_to_wallet(self):
        self.wallet.append(KeyPair.gen_keypair())

    def update_balance(self, delta: int):
        self.balance += delta

    def get_balance(self):
        return self.balance

    def print_balance(self):
        print(f"[{self.account_id}] balance = {self.balance}")

    def sign_data(self, message: str, key_index: int = 0) -> str:
        return Signature.sign_data(self.wallet[key_index].private_key, message)

    def create_payment_op(self, receiver, amount: int, key_index: int = 0):
        from operation import Operation
        return Operation.create_operation(self, receiver, amount, key_index)