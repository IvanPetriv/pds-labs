import secrets
import struct

from abc import ABC, abstractmethod


__all__ = ["RC5"]


class RC5(ABC):
    mode: str = "RC5_CBC_PAD"
    word_len: int
    round_num: int
    key_len: int
    block_size: int = None

    # Constants for RC5 Key Expansion
    P32 = 0xB7E15163
    Q32 = 0x9E3779B9

    @classmethod
    def set_parameters(cls, word_len: int, rounds: int, key_len: int) -> None:
        """
        Sets starting parameters for encryption and decryption
        :param word_len: Length of the word in bits
        :param rounds: Number of rounds for encrypting/decrypting
        :param key_len: Length of the key
        """
        cls.word_len = word_len
        cls.round_num = rounds
        cls.key_len = key_len
        cls.block_size = 2 * (word_len // 8)  # Block size (64 bits)

    @classmethod
    @abstractmethod
    def encrypt(cls, plaintext, key, iv) -> str:
        pass

    @classmethod
    @abstractmethod
    def decrypt(cls, plaintext, key, iv) -> str:
        pass

    @classmethod
    def __encrypt_block(cls, plain_block, S):
        A, B = struct.unpack('<II', plain_block)
        A = (A + S[0]) & 0xFFFFFFFF
        B = (B + S[1]) & 0xFFFFFFFF
        for i in range(1, cls.round_num + 1):
            A = ((A ^ B) << B % 32 | (A ^ B) >> (32 - (B % 32))) & 0xFFFFFFFF
            A = (A + S[2 * i]) & 0xFFFFFFFF
            B = ((B ^ A) << A % 32 | (B ^ A) >> (32 - (A % 32))) & 0xFFFFFFFF
            B = (B + S[2 * i + 1]) & 0xFFFFFFFF
        return struct.pack('<II', A, B)

    @classmethod
    def __decrypt_block(cls, cipher_block, S):
        A, B = struct.unpack('<II', cipher_block)
        for i in range(cls.round_num, 0, -1):
            B = (B - S[2 * i + 1]) & 0xFFFFFFFF
            B = ((B >> A % 32 | B << (32 - (A % 32))) & 0xFFFFFFFF) ^ A
            A = (A - S[2 * i]) & 0xFFFFFFFF
            A = ((A >> B % 32 | A << (32 - (B % 32))) & 0xFFFFFFFF) ^ B
        B = (B - S[1]) & 0xFFFFFFFF
        A = (A - S[0]) & 0xFFFFFFFF
        return struct.pack('<II', A, B)

    @classmethod
    def pad(cls, data, block_size):
        padding_len = block_size - len(data) % block_size
        return data + bytes([padding_len]) * padding_len

    @classmethod
    def unpad(cls, data):
        padding_len = data[-1]
        return data[:-padding_len]

    @classmethod
    def __key_expansion(cls, key):
        # Convert the key to an array of W-bit words
        L = [0] * (cls.key_len // 4)
        for i in range(cls.key_len):
            L[i // 4] = L[i // 4] | (key[i] << (8 * (i % 4)))

        # Initialize the subkeys array
        S = [(cls.P32 + i * cls.Q32) & 0xFFFFFFFF for i in range(2 * (cls.round_num + 1))]

        # Key mixing process
        i = j = A = B = 0
        for _ in range(3 * max(len(S), len(L))):
            A = S[i] = ((S[i] + A + B) << 3) & 0xFFFFFFFF
            B = L[j] = ((L[j] + A + B) << (A + B) % 32) & 0xFFFFFFFF
            i = (i + 1) % len(S)
            j = (j + 1) % len(L)

        return S


class RC5_CBC_PAD(RC5):

    @classmethod
    def encrypt(cls, plaintext, key, iv):
        S = cls.__key_expansion(key)
        plaintext = cls.pad(plaintext, cls.block_size)
        ciphertext = b''
        prev_block = iv

        for i in range(0, len(plaintext), cls.block_size):
            block = plaintext[i:i + cls.block_size]
            xor_block = bytes([_a ^ _b for _a, _b in zip(block, prev_block)])
            encrypted_block = cls.__encrypt_block(xor_block, S)
            ciphertext += encrypted_block
            prev_block = encrypted_block

        return ciphertext

    @classmethod
    def decrypt(cls, ciphertext, key, iv):
        S = cls.__key_expansion(key)
        plaintext = b''
        prev_block = iv

        for i in range(0, len(ciphertext), cls.block_size):
            block = ciphertext[i:i + cls.block_size]
            decrypted_block = cls.__decrypt_block(block, S)
            xor_block = bytes([_a ^ _b for _a, _b in zip(decrypted_block, prev_block)])
            plaintext += xor_block
            prev_block = block

        return cls.unpad(plaintext)





if __name__ == "__main__":
    RC5.set_parameters(16, 20, 8)
    message = b"Confidential message for encryption!"
    print("Original message:", message)

    key = secrets.token_bytes(8)
    iv = secrets.token_bytes(2 * (16 // 8))

    # Encrypt
    ciphertext = RC5_CBC_PAD.encrypt(message, key, iv)
    print("Ciphertext:", ciphertext)

    # Decrypt
    decrypted_message = RC5_CBC_PAD.decrypt(ciphertext, key, iv)
    print("Decrypted message:", decrypted_message)
