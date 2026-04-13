from dataclasses import dataclass
from account import Account
from signature import Signature

@dataclass
class Operation:
    sender_id: str
    receiver_id: str
    amount: int
    sender_pubkey: str
    signature: str

    @staticmethod
    def _message(sender_id: str, receiver_id: str, amount: int) -> str:
        return f"{sender_id}->{receiver_id}:{amount}"

    @staticmethod
    def create_operation(sender: Account, receiver: Account, amount: int, key_index: int = 0):
        message = Operation._message(sender.account_id, receiver.account_id, amount)
        signature = sender.sign_data(message, key_index)
        return Operation(
            sender_id=sender.account_id,
            receiver_id=receiver.account_id,
            amount=amount,
            sender_pubkey=sender.wallet[key_index].public_key,
            signature=signature
        )

    def verify_operation(self, sender_account: Account) -> bool:
        if self.amount <= 0:
            return False

        kp = None
        for k in sender_account.wallet:
            if k.public_key == self.sender_pubkey:
                kp = k
                break
        if kp is None:
            return False

        msg = Operation._message(self.sender_id, self.receiver_id, self.amount)
        return Signature.verify_signature(self.signature, kp, msg)