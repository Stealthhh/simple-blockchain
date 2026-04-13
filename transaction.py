import json
from dataclasses import dataclass
from typing import List
from operation import Operation
from hash_util import sha256_str

@dataclass
class Transaction:
    operations: List[Operation]
    nonce: int
    transaction_id: str = ""

    @staticmethod
    def create_transaction(operations: List[Operation], nonce: int):
        tx = Transaction(operations=operations, nonce=nonce)
        tx.transaction_id = tx.calculate_id()
        return tx

    def calculate_id(self) -> str:
        payload = {
            "operations": [op.__dict__ for op in self.operations],
            "nonce": self.nonce
        }
        return sha256_str(json.dumps(payload, sort_keys=True))