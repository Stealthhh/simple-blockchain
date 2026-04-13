import secrets
from dataclasses import dataclass
from hash_util import sha256_str

@dataclass
class KeyPair:
    private_key: str
    public_key: str

    @staticmethod
    def gen_keypair():
        private_key = secrets.token_hex(32)
        public_key = sha256_str(private_key)
        return KeyPair(private_key=private_key, public_key=public_key)

    def print_keypair(self):
        print(f"PrivateKey: {self.private_key}")
        print(f"PublicKey : {self.public_key}")