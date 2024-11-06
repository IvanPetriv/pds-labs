import unittest
import os
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from dss import Dss  # Assuming the Dss class is saved in dss.py


class TestDss(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.message = b"Test message for digital signature."
        cls.private_key, cls.public_key = Dss.generate_key_pair()
        cls.signature = Dss.sign_message(cls.message, cls.private_key)

    def test_generate_key_pair(self):
        private_key, public_key = Dss.generate_key_pair()
        self.assertIsInstance(private_key, RSA.RsaKey)
        self.assertIsInstance(public_key, RSA.RsaKey)
        self.assertNotEqual(private_key, public_key)

    def test_save_and_load_private_key(self):
        # Save and load private key
        Dss.save_key_to_file(self.private_key, 'private_key.pem', private=True)
        loaded_private_key = Dss.load_key_from_file('private_key.pem')
        self.assertEqual(self.private_key.export_key(), loaded_private_key.export_key())

    def test_save_and_load_public_key(self):
        # Save and load public key
        Dss.save_key_to_file(self.public_key, 'public_key.pem', private=False)
        loaded_public_key = Dss.load_key_from_file('public_key.pem')
        self.assertEqual(self.public_key.export_key(), loaded_public_key.export_key())

    def test_sign_message(self):
        # Ensure the signature is a non-empty byte string
        signature = Dss.sign_message(self.message, self.private_key)
        self.assertIsInstance(signature, bytes)
        self.assertGreater(len(signature), 0)

    def test_verify_signature_valid(self):
        # Check if a valid signature is correctly verified
        self.assertTrue(Dss.verify_signature(self.message, self.signature, self.public_key))

    def test_verify_signature_invalid(self):
        # Check if an invalid signature fails verification
        altered_message = b"Tampered message for digital signature."
        self.assertFalse(Dss.verify_signature(altered_message, self.signature, self.public_key))

    def test_verify_signature_wrong_key(self):
        # Check verification with a wrong public key
        another_private_key, another_public_key = Dss.generate_key_pair()
        self.assertFalse(Dss.verify_signature(self.message, self.signature, another_public_key))

    @classmethod
    def tearDownClass(cls):
        # Clean up key files
        for filename in ['private_key.pem', 'public_key.pem']:
            if os.path.exists(filename):
                os.remove(filename)


if __name__ == "__main__":
    unittest.main()
