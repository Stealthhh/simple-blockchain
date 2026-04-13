from keypair import KeyPair
from hash_util import sha256_str

class Signature:
    @staticmethod
    def sign_data(private_key: str, message: str) -> str:
        return sha256_str(private_key + message)

    @staticmethod
    def verify_signature(signature: str, keypair: KeyPair, message: str) -> bool:
        expected = Signature.sign_data(keypair.private_key, message)
        return signature == expected