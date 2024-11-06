from __future__ import annotations

import math
import random
from abc import ABC, abstractmethod

from model import lcg_model


default_encoding: str = "utf-8"


class RC5(ABC):
    def __init__(self, word_size: int = 32, round_count: int = 12, key_size: int = 16):
        """
        :param word_size: Size of a word in bits (16, 32 or 64, default 32)
        :param round_count: Number of rounds to perform (between 0 and 255, default 12)
        :param key_size: Size of a key (between 0 and 255, default 16)
        """
        if word_size not in {16, 32, 64}:
            raise ValueError("'word_size' must be 16, 32 or 64")
        if round_count not in range(0, 256):
            raise ValueError("'round_count' must be in range between 0 and 255")
        if key_size not in range(0, 256):
            raise ValueError("'key_size' must be in range between 0 and 255")

        self._word_size_bits: int = word_size
        self._round_count: int = round_count
        self._key_size: int = key_size

    @property
    def _word_size_bytes(self) -> int:
        return self._word_size_bits // 8

    @property
    def _byte_mask(self) -> int:
        return (1 << self._word_size_bits) - 1

    @property
    def _p(self) -> int:
        """
        :return: Constant derived from Euler's number
        """
        match self._word_size_bits:
            case 16:
                return 0xB7E1
            case 32:
                return 0xB7E15163
            case 64:
                return 0xB7E151638AED2A6B

    @property
    def _q(self) -> int:
        """
        :return: Constant derived from Golden ratio
        """
        match self._word_size_bits:
            case 16:
                return 0x9E37
            case 32:
                return 0x9E3779B9
            case 64:
                return 0x9E3779B97F4A7C15

    def _rotl(self, x: int, y: int) -> int:
        y %= self._word_size_bits
        return (x << y) & self._byte_mask | ((x & self._byte_mask) >> (self._word_size_bits - y))

    def _rotr(self, x: int, y: int) -> int:
        y %= self._word_size_bits
        return ((x & self._byte_mask) >> y) | (x << (self._word_size_bits - y) & self._byte_mask)

    @abstractmethod
    def encrypt(self, text: str, key: str, encoding: str = default_encoding) -> str:
        ...

    @abstractmethod
    def decrypt(self, text: str, key: str, encoding: str = default_encoding) -> str:
        ...

    def _encrypt_block(self, A: int, B: int, S: list[int]) -> tuple[int, int]:
        """
        Algorithm:

        * Take a block of text and divide it into two halves (A and B)
        *
        :param A: First half of the block
        :param B: Second half of the block
        :param S: Key expansion
        :return: Two halves of the block back
        """
        A = (A + S[0]) & self._byte_mask
        B = (B + S[1]) & self._byte_mask

        for i in range(1, self._round_count + 1):
            A = (self._rotl(A ^ B, B) + S[2 * i]) & self._byte_mask
            B = (self._rotl(B ^ A, A) + S[2 * i + 1]) & self._byte_mask

        return A, B

    def _decrypt_block(self, A: int, B: int, S: list[int]) -> tuple[int, int]:
        for i in range(self._round_count, 0, -1):
            B = (self._rotr(B - S[2 * i + 1], A)) ^ A
            A = (self._rotr(A - S[2 * i], B)) ^ B

        B = (B - S[1]) & self._byte_mask
        A = (A - S[0]) & self._byte_mask

        return A, B

    def _generate_key_expansion(self, key: bytes) -> list[int]:
        """
        Shuffles the key to make it usable in encryption.

        Algorithm:

        * Initialize L with key divided into words
        * Initialize S with arbitrary values (derived from e and phi)
        * Mix them
        :param key: Key to use in shuffling
        :return: Shuffled list of words
        """
        L: list[int] = [0] * math.ceil(len(key) / self._word_size_bytes)
        for i in range(self._key_size - 1, -1, -1):
            L[i // self._word_size_bytes] = (L[i // self._word_size_bytes] << 8) + key[i]

        S: list[int] = [self._p]
        for i in range(1, 2 * (self._round_count + 1)):
            S.append((S[i - 1] + self._q) & self._byte_mask)

        A = B = 0
        i = j = 0
        for k in range(3 * max(len(S), len(L))):
            A = S[i] = self._rotl((S[i] + A + B) & self._byte_mask, 3)
            B = L[j] = self._rotl((L[j] + A + B) & self._byte_mask, A + B)

            i = (i + 1) % len(S)
            j = (j + 1) % len(L)

        return S


class RC5_CBC_PAD(RC5):
    def encrypt(self, text: str | bytes, key: str | bytes, encoding: str = default_encoding) -> str:
        key: bytes = bytes(key, encoding) if type(key) is str else key
        text: bytes = self._pad_text(bytes(text, encoding) if type(text) is str else text)
        encrypted_text: bytearray = bytearray()

        block_size_bytes: int = self._word_size_bytes * 2
        key_expansion: list[int] = self._generate_key_expansion(key)
        iv: bytes = self._generate_iv()
        tempA, tempB = self._encrypt_block(int.from_bytes(iv[:self._word_size_bytes], "big"),
                                           int.from_bytes(iv[self._word_size_bytes:], "big"),
                                           key_expansion)
        encrypted_iv = (tempA.to_bytes(self._word_size_bytes, 'big')
                        + tempB.to_bytes(self._word_size_bytes, 'big'))
        print(f"IV: {iv.hex()}")
        previous_block: bytes = iv

        # Divides the text into blocks
        for i in range(0, len(text), block_size_bytes):
            current_block: bytes = text[i:i + block_size_bytes]
            current_xor_block: bytes = bytes([_a ^ _b for _a, _b in zip(current_block, previous_block)])
            A, B = self._encrypt_block(int.from_bytes(current_xor_block[:self._word_size_bytes], "big"),
                                       int.from_bytes(current_xor_block[self._word_size_bytes:], "big"),
                                       key_expansion)

            previous_block = (A.to_bytes(self._word_size_bytes, 'big')
                              + B.to_bytes(self._word_size_bytes, 'big'))

            encrypted_text += previous_block
        encrypted_text = bytearray(encrypted_iv) + encrypted_text
        return encrypted_text.hex()

    def decrypt(self, text: str | bytes, key: str | bytes, encoding: str = default_encoding) -> bytes:
        key: bytes = bytes(key, encoding) if type(key) is str else key
        text: bytes = bytes.fromhex(text) if type(text) is str else bytes.fromhex(text.decode(encoding))
        decrypted_text: bytearray = bytearray()

        block_size_bytes: int = self._word_size_bytes * 2
        key_expansion: list[int] = self._generate_key_expansion(key)
        tempA, tempB = self._decrypt_block(int.from_bytes(text[:self._word_size_bytes], "big"),
                                           int.from_bytes(text[self._word_size_bytes:block_size_bytes], "big"),
                                           key_expansion)
        iv: bytes = (tempA.to_bytes(self._word_size_bytes, 'big')
                     + tempB.to_bytes(self._word_size_bytes, 'big'))

        previous_block: bytes = iv

        for i in range(block_size_bytes, len(text), block_size_bytes):
            current_block: bytes = text[i:i + block_size_bytes]
            A, B = self._decrypt_block(int.from_bytes(current_block[:self._word_size_bytes], "big"),
                                       int.from_bytes(current_block[self._word_size_bytes:], "big"),
                                       key_expansion)
            decrypted_block: bytes = (A.to_bytes(self._word_size_bytes, 'big')
                                      + B.to_bytes(self._word_size_bytes, 'big'))
            current_xor_block: bytes = bytes([_a ^ _b for _a, _b in zip(decrypted_block, previous_block)])
            decrypted_text += current_xor_block
            previous_block = current_block

        return self._unpad_text(decrypted_text)

    def _pad_text(self, text: bytes, mode: str = "pkcs7") -> bytes:
        match mode.lower():
            case "pkcs7":  # All padding bytes are the length to pad
                padding_len: int = self._word_size_bytes * 2 - len(text) % (self._word_size_bytes * 2)
                padding: bytes = bytes([padding_len for _ in range(padding_len)])
                return text + padding
            case _:
                raise ValueError(f"Unknown mode for text padding: {mode}")

    def _unpad_text(self, text: bytes, mode: str = "pkcs7") -> bytes:
        match mode.lower():
            case "pkcs7":  # All padding bytes are the length to pad
                padding_len: int = text[-1]
                return text[:-padding_len]
            case _:
                raise ValueError(f"Unknown mode for text unpadding: {mode}")

    def _generate_iv(self) -> bytes:
        """
        Generates an initialization vector with LCG algorithm
        :return: Initialization vector
        """
        iv: bytearray = bytearray()

        for n in lcg_model.generate_sequence(random.randint(2 ** 25 - 1, 2**31-1),
                                             random.randint(12 ** 3, 12**5), random.randint(200, 20000),
                                             random.randint(10, 10000)):
            if len(iv) >= self._word_size_bytes * 2:
                break
            iv.append(n & 255)
        return bytes(iv)


if __name__ == "__main__":
    algo = RC5_CBC_PAD()
    result = algo.encrypt("text", "keylendd")
    print(f"Encryption: {result}")
    result = algo.decrypt(result, "keylendd")
    print(f"Decryption: {result}")
