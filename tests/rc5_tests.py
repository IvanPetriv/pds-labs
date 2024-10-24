import unittest as ut
from model import rc5_model


class TestRc5(ut.TestCase):
    def setUp(self):
        # Test case: (word_size, round_count, key_size, text, key, encrypted_text)
        self.test_cases = [
            (32, 12, 16, "8-chars.", "8-chars,", None),
            (32, 255, 16, "encrypted text", "8-,", None),
            (32, 12, 255, "8-chars.", "8-chars,", None),
            (32, 12, 0, "8-chars.", "8-chars,", None),
            (32, 0, 16, "8-chars.", "8-chars,", None),
            (16, 12, 16, "8-chars.", "8-chars,", None),
            (16, 255, 16, "8-chars.", "8-chars,", None),
            (16, 12, 255, "8-chars.", "8-chars,", None),
            (16, 12, 0, "8-chars.", "8-chars,", None),
            (16, 0, 16, "8-chars.", "8-chars,", None),
            (64, 12, 16, "A very long encryption text", "1", None),
            (64, 255, 16, "8.", "8-regerghethjsrjmsymjytsmtsyhmmzm,", None),
            (64, 12, 255, "8-chars.", "8-chars,", None),
            (64, 12, 0, "8-chars.", "8-chars,", None),
            (64, 12, 16, "", "8-chars,", None),
            (64, 12, 16, "8-chars.", "", None),
            (64, 12, 16, "", "", None),
            (64, 12, 16, "", " ", None),
            (16, 20, 8, "Hello, this is my variant", "putinkhuilo", None),
        ]

        # Test case: (word_size, round_count, key_size, text, key, exception)
        self.test_cases_exceptions = [
            (32, 256, 16, "8-chars.", "8-chars,", ValueError),
            (32, 12, 256, "8-chars.", "8-chars,", ValueError),
            (26, 12, 16, "8-chars.", "8-chars,", ValueError),
            (0, 0, 0, "8-chars.", "8-chars,", ValueError),
        ]

    def test_values(self):
        for word_size, round_count, key_size, text, key, encrypted_text in self.test_cases:
            with self.subTest(word_size=word_size,
                              round_count=round_count,
                              key_size=key_size,
                              text=text,
                              key=key,
                              encrypted_text=encrypted_text):
                algo = rc5_model.RC5_CBC_PAD(word_size, round_count, key_size)
                calculated_encrypted_text = algo.encrypt(text, key)
                calculated_decrypted_text = algo.decrypt(calculated_encrypted_text, key)

                self.assertEqual(text, calculated_decrypted_text)
                # self.assertEqual(encrypted_text, calculated_encrypted_text)

    def test_exceptions(self):
        for word_size, round_count, key_size, text, key, exception in self.test_cases_exceptions:
            with self.subTest(word_size=word_size,
                              round_count=round_count,
                              key_size=key_size,
                              text=text,
                              key=key,
                              exception=exception):
                algo = rc5_model.RC5_CBC_PAD(word_size, round_count, key_size)
                calculated_encrypted_text = algo.encrypt(text, key)
                calculated_decrypted_text = algo.decrypt(calculated_encrypted_text, key)

                self.assertRaises(exception)


if __name__ == "__main__":
    ut.main(verbosity=2)
