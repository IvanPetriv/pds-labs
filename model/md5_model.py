from __future__ import annotations

from collections.abc import Callable
import math


class Md5:
    """
    A static class that gives an ``md5`` function to calculate MD5 hash from the string.
    """

    # This list contains a start value for buffers
    __init_MDBuffer: list[int] = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]

    # This list maintains the amount by which to rotate the buffers during processing stage
    __rotate_by = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                   5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
                   4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                   6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]

    # This list maintains the additive constant to be added in each processing step.
    __constants = [int(abs(math.sin(i + 1)) * 4294967296) & 0xFFFFFFFF for i in range(64)]

    @staticmethod
    def __pad(msg: str | bytearray) -> bytearray:
        """
        Appends padding bits so its length is congruent to 448 % 512.
        After that it appends the length of the message in lower 64 bits
        :return: A bytearray (length is multiple of 64)
        """
        # Appends padding
        if type(msg) is str:
            msg: bytearray = bytearray(msg, "utf-8")
        if type(msg) is not None:
            msg: bytearray = bytearray(msg)
        msg_len_in_bits: int = (8 * len(msg)) & 0xffffffffffffffff
        msg.append(0x80)

        while len(msg) % 64 != 56:
            msg.append(0)

        # Appends the length of the message (little endian convention)
        msg += msg_len_in_bits.to_bytes(8, byteorder='little')

        return msg

    @staticmethod
    def __hash_message(msg: bytearray) -> int:
        def leftRotate(x, amount):
            x &= 0xFFFFFFFF
            return (x << amount | x >> (32 - amount)) & 0xFFFFFFFF

        # Logical functions to apply
        fF: Callable = lambda b, c, d: (b & c) | (~b & d)
        fG: Callable = lambda b, c, d: (b & d) | (~d & c)
        fH: Callable = lambda b, c, d: b ^ c ^ d
        fI: Callable = lambda b, c, d: c ^ (b | ~d)

        # Permutations
        pF: Callable = lambda i: i
        pG: Callable = lambda i: (5 * i + 1) % 16
        pH: Callable = lambda i: (3 * i + 5) % 16
        pI: Callable = lambda i: (7 * i) % 16

        init_buffer = Md5.__init_MDBuffer.copy()
        # Divides the message into 64-byte chunks
        for offset in range(0, len(msg), 64):
            block = msg[offset: offset + 64]  # creates block to be processed
            A, B, C, D = init_buffer

            for i in range(64):
                if i < 16:
                    func, index_func = fF, pF
                elif i < 32:
                    func, index_func = fG, pG
                elif i < 48:
                    func, index_func = fH, pH
                else:
                    func, index_func = fI, pI

                F = func(B, C, D)
                G = index_func(i)

                to_rotate = A + F + Md5.__constants[i] + int.from_bytes(block[4 * G: 4 * G + 4], byteorder='little')
                newB = (B + leftRotate(to_rotate, Md5.__rotate_by[i])) & 0xFFFFFFFF

                A, B, C, D = D, newB, B, C

            for i, val in enumerate([A, B, C, D]):
                init_buffer[i] += val
                init_buffer[i] &= 0xFFFFFFFF

        return sum(buffer_content << (32 * i) for i, buffer_content in enumerate(init_buffer))

    @staticmethod
    def __MD_to_hex(digest):
        # takes MD from the processing stage, change its endian-ness and return it as 128-bit hex hash
        raw = digest.to_bytes(16, byteorder='little')
        return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))

    @staticmethod
    def md5(msg: str) -> str:
        msg = Md5.__pad(msg)
        processed_msg = Md5.__hash_message(msg)
        # processed_msg contains the integer value of the hash
        message_hash = Md5.__MD_to_hex(processed_msg)
        print(f"Message Hash: {message_hash}")
        return message_hash


if __name__ == '__main__':
    message = input()
    Md5.md5(message)
