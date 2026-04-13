from account import Account
from transaction import Transaction
from block import Block
from blockchain import Blockchain

def main():
    print("Blockchain:")

    blockchain = Blockchain.init_blockchain()

    name1 = Account.gen_account()
    name2 = Account.gen_account()
    accounts = {name1.account_id: name1, name2.account_id: name2}

    blockchain.get_token_from_faucet(name1, 120)
    blockchain.get_token_from_faucet(name2, 30)

    print(f"Name1 ID: {name1.account_id}")
    print(f"Name2 ID  : {name2.account_id}")
    name1.print_balance()
    name2.print_balance()

    op1 = name1.create_payment_op(name2, 50, 0)
    tx1 = Transaction.create_transaction([op1], nonce=1)

    prev_hash = blockchain.block_history[-1].block_id
    block1 = Block.create_block([tx1], prev_hash)

    blockchain.validate_block(block1, accounts)

    print("\nAfter block:")
    name1.print_balance()
    name2.print_balance()
    blockchain.show_coin_database()
    print(f"\nBlocks: {len(blockchain.block_history)}")
    print(f"Tx in DB: {len(blockchain.tx_database)}")

if __name__ == "__main__":
    main()