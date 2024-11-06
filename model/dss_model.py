from Crypto.Hash.SHA256 import SHA256Hash
from Crypto.PublicKey import RSA
from Crypto.PublicKey.RSA import RsaKey
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256


class Dss:
    @staticmethod
    def generate_key_pair(bits: int = 2048) -> tuple[RsaKey, RsaKey]:
        private_key = RSA.generate(bits)
        return private_key, private_key.public_key()

    @staticmethod
    def save_key_to_file(key: RsaKey, filename: str, private: bool = False) -> None:
        with open(filename, 'wb') as file:
            file_content = (key.export_key(format='PEM', pkcs=8)
                            if private else
                            key.publickey().export_key(format='PEM'))
            file.write(file_content)

    @staticmethod
    def load_key_from_file(filename: str) -> RsaKey:
        with open(filename, 'rb') as file:
            return RSA.import_key(file.read())

    @staticmethod
    def sign_message(message: bytes, private_key: RsaKey) -> bytes:
        hash_obj: SHA256Hash = SHA256.new(message)
        signature = pkcs1_15.new(private_key).sign(hash_obj)
        return signature

    @staticmethod
    def verify_signature(message: bytes, signature: bytes, public_key: RsaKey) -> bool:
        hashed_message: SHA256Hash = SHA256.new(message)
        try:
            pkcs1_15.new(public_key).verify(hashed_message, signature)
            return True
        except (ValueError, TypeError):
            return False
