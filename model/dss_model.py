from Crypto.PublicKey import DSA
from Crypto.Signature import DSS
from Crypto.Hash import SHA256


class Dss:
    @staticmethod
    def generate_key_pair(bits: int = 1_024) -> tuple[DSA.DsaKey, DSA.DsaKey]:
        private_key = DSA.generate(bits)
        return private_key, private_key.public_key()

    @staticmethod
    def save_key_to_file(key: DSA.DsaKey, filename: str, private: bool = False) -> None:
        with open(filename, 'wb') as file:
            file_content = (key.export_key(format='PEM')
                            if private else
                            key.public_key().export_key(format='PEM'))
            file.write(file_content)

    @staticmethod
    def load_key_from_file(filename: str) -> DSA.DsaKey:
        with open(filename, 'rb') as file:
            return DSA.import_key(file.read())

    @staticmethod
    def sign_message(message: bytes, private_key: DSA.DsaKey) -> bytes:
        hash_obj = SHA256.new(message)
        signer = DSS.new(private_key, 'fips-186-3')
        return signer.sign(hash_obj)

    @staticmethod
    def verify_signature(message: bytes, signature: bytes, public_key: DSA.DsaKey) -> bool:
        hashed_message = SHA256.new(message)
        verifier = DSS.new(public_key, 'fips-186-3')
        try:
            verifier.verify(hashed_message, signature)
            return True
        except ValueError as e:
            print(e)
            return False


if __name__ == "__main__":
    message = b"massage"
    private_key, public_key = Dss.generate_key_pair()
    signature = Dss.sign_message(message, private_key)
    verification = Dss.verify_signature(message, signature, public_key)
    print(verification)
