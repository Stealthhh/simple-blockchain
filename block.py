import json
import time
from dataclasses import dataclass
from typing import List
from transaction import Transaction
from hash_util import sha256_str

@dataclass
class Block:
    prev_hash: str
    transactions: List[Transaction]
    timestamp: float
    block_id: str = ""

    @staticmethod
    def create_block(transactions: List[Transaction], prev_hash: str):
        block = Block(prev_hash=prev_hash, transactions=transactions, timestamp=time.time())
        block.block_id = block.calculate_id()
        return block

    def calculate_id(self) -> str:
        payload = {
            "prev_hash": self.prev_hash,
            "transactions": [tx.transaction_id for tx in self.transactions],
            "timestamp": self.timestamp
        }
        return sha256_str(json.dumps(payload, sort_keys=True))