from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey.RSA import RsaKey
from typing import Tuple


class Rsa:
    @staticmethod
    def generate_key_pair(bits: int = 1024) -> Tuple[RsaKey, RsaKey]:
        key = RSA.generate(bits)
        return key, key.public_key()

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
    def encrypt(text: bytes, public_key: RsaKey) -> bytes:
        cipher_rsa = PKCS1_OAEP.new(public_key)
        ciphertext = cipher_rsa.encrypt(text)
        return ciphertext

    @staticmethod
    def decrypt(ciphertext: bytes, private_key: RsaKey) -> bytes:
        decryptor_rsa = PKCS1_OAEP.new(private_key)
        decrypted_message = decryptor_rsa.decrypt(ciphertext)
        return decrypted_message


if __name__ == "__main__":
    # Example usage:
    # Generate and save keys
    private_key, public_key = Rsa.generate_key_pair()
    Rsa.save_key_to_file(private_key, 'private_key.pem', private=True)
    Rsa.save_key_to_file(public_key, 'public_key.pem', private=False)

    # Load keys from files
    loaded_private_key = Rsa.load_key_from_file('private_key.pem')
    loaded_public_key = Rsa.load_key_from_file('public_key.pem')

    # Encrypt a message using the loaded public key
    message = (b"Hello, RSA Encryption with file storage!"
               b"111111111111111111111111111111111111111111111111111111111111111111111111111111111111"
               b"111111111111111111111111111111111111111111111111111111111111111111111111111111")
    encrypted_message = Rsa.encrypt(message, loaded_public_key)
    print("Encrypted message:", encrypted_message.hex())

    # Decrypt the message using the loaded private key
    decrypted_message = Rsa.decrypt(encrypted_message, loaded_private_key)
    print("Decrypted message:", decrypted_message)
