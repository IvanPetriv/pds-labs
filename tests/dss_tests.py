import unittest
import os
from Crypto.PublicKey import DSA
from model.dss_model import Dss


class TestDss(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Generate keys for testing
        cls.private_key, cls.public_key = Dss.generate_key_pair()
        cls.message = b"This is a test message."
        cls.signature = Dss.sign_message(cls.message, cls.private_key)
        cls.private_key_file = "test_private_key.pem"
        cls.public_key_file = "test_public_key.pem"

    def test_generate_key_pair(self):
        private_key, public_key = Dss.generate_key_pair()
        self.assertIsInstance(private_key, DSA.DsaKey)
        self.assertIsInstance(public_key, DSA.DsaKey)
        self.assertTrue(private_key.has_private())
        self.assertFalse(public_key.has_private())

    def test_save_and_load_private_key(self):
        # Save and load the private key
        Dss.save_key_to_file(self.private_key, self.private_key_file, private=True)
        loaded_private_key = Dss.load_key_from_file(self.private_key_file)
        self.assertEqual(self.private_key.export_key(), loaded_private_key.export_key())

    def test_save_and_load_public_key(self):
        # Save and load the public key
        Dss.save_key_to_file(self.public_key, self.public_key_file, private=False)
        loaded_public_key = Dss.load_key_from_file(self.public_key_file)
        self.assertEqual(self.public_key.export_key(), loaded_public_key.export_key())

    def test_sign_message(self):
        # Ensure that signing a message returns a signature
        signature = Dss.sign_message(self.message, self.private_key)
        self.assertIsInstance(signature, bytes)
        self.assertNotEqual(signature, b'')

    def test_verify_signature_valid(self):
        # Check that the signature is valid
        self.assertTrue(Dss.verify_signature(self.message, self.signature, self.public_key))

    def test_verify_signature_invalid(self):
        # Check that modifying the message or signature invalidates it
        tampered_message = b"This is a tampered message."
        tampered_signature = self.signature[:-1] + (b'\x00' if self.signature[-1] != b'\x00' else b'\x01')
        self.assertFalse(Dss.verify_signature(tampered_message, self.signature, self.public_key))
        self.assertFalse(Dss.verify_signature(self.message, tampered_signature, self.public_key))

    @classmethod
    def tearDownClass(cls):
        # Clean up test files
        if os.path.exists(cls.private_key_file):
            os.remove(cls.private_key_file)
        if os.path.exists(cls.public_key_file):
            os.remove(cls.public_key_file)


if __name__ == "__main__":
    unittest.main()
