from typing import Dict, List, Set
from account import Account
from block import Block

class Blockchain:
    def __init__(self, faucet_coins: int = 100):
        self.coin_database: Dict[str, int] = {}
        self.block_history: List[Block] = []
        self.tx_database: Set[str] = set()
        self.faucet_coins = faucet_coins

    @staticmethod
    def init_blockchain():
        bc = Blockchain()
        genesis = Block.create_block(transactions=[], prev_hash="0" * 64)
        bc.block_history.append(genesis)
        return bc

    def get_token_from_faucet(self, account: Account, amount: int = None):
        if amount is None:
            amount = self.faucet_coins
        self.coin_database[account.account_id] = self.coin_database.get(account.account_id, 0) + amount
        account.update_balance(amount)

    def show_coin_database(self):
        print("\nCOIN DATABASE:")
        for acc_id, bal in self.coin_database.items():
            print(f"{acc_id}: {bal}")

    def validate_block(self, block: Block, accounts: Dict[str, Account]) -> bool:
        last_block = self.block_history[-1]
        if block.prev_hash != last_block.block_id:
            print("Block rejected: wrong prev_hash")
            return False

        temp_balances = dict(self.coin_database)

        for tx in block.transactions:
            if tx.transaction_id in self.tx_database:
                print("Block rejected: duplicate transaction")
                return False

            for op in tx.operations:
                if op.sender_id not in accounts or op.receiver_id not in accounts:
                    print("Block rejected: unknown account")
                    return False

                sender = accounts[op.sender_id]
                receiver = accounts[op.receiver_id]

                if not op.verify_operation(sender):
                    print("Block rejected: bad signature")
                    return False

                sender_balance = temp_balances.get(sender.account_id, 0)
                if op.amount > sender_balance:
                    print("Block rejected: insufficient funds")
                    return False

                temp_balances[sender.account_id] = sender_balance - op.amount
                temp_balances[receiver.account_id] = temp_balances.get(receiver.account_id, 0) + op.amount

        self.coin_database = temp_balances
        for tx in block.transactions:
            self.tx_database.add(tx.transaction_id)
        self.block_history.append(block)

        for acc_id, acc in accounts.items():
            acc.balance = self.coin_database.get(acc_id, 0)

        print("Block accepted")
        return True