"""
These are the test cases for the Encrypt project

Name: Dominik Pathuis

Date: 9/23/2024

Version: Python 3.9
"""

import unittest
from encrypt import (Salting, ReverseCipher1, ReverseCipher2, XORCipher, CaesarCipher, VigenereCipher,
                     CustomMappingCipher)


class CipherTests(unittest.TestCase):
    def test_salting(self):
        my_salt = Salting('Hello', 'gvsulakers')
        self.assertEqual(str(my_salt), 'Hello')
        self.assertEqual(my_salt.cipher_text, 'Hello' + 'gvsulakers')

        with self.assertRaises(TypeError):
            Salting(123, 'gvsulakers')
        with self.assertRaises(TypeError):
            Salting('Hello', 123)

    def test_reverse_cipher1(self):
        rev1 = ReverseCipher1('Hello')
        self.assertEqual(str(rev1), 'Hello')
        self.assertEqual(rev1.cipher_text, 'olleH')

        with self.assertRaises(TypeError):
            ReverseCipher1(123)

    def test_reverse_cipher2(self):
        rev2 = ReverseCipher2('Hello World')
        self.assertEqual(str(rev2), 'Hello World')
        self.assertEqual(rev2.cipher_text, 'olleH dlroW')

        with self.assertRaises(TypeError):
            ReverseCipher2(123)

    def test_xor_cipher(self):
        xor1 = XORCipher('Hello, Students', 'gvsu')
        self.assertEqual(str(xor1), 'Hello, Students')
        self.assertEqual(xor1.cipher_text[5:8], 'ZS&')

        with self.assertRaises(TypeError):
            XORCipher(123, 'gvsu')
        with self.assertRaises(TypeError):
            XORCipher('Hello, Students', 123)

    def test_caesar_cipher(self):
        caesar = CaesarCipher('HELLO', 3)
        self.assertEqual(str(caesar), 'HELLO')
        self.assertEqual(caesar.cipher_text, 'KHOOR')

        with self.assertRaises(TypeError):
            CaesarCipher(123, 3)
        with self.assertRaises(TypeError):
            CaesarCipher('HELLO', 'three')

    def test_vigenere_cipher(self):
        vigenere = VigenereCipher('HELLO', 'KEY')
        self.assertEqual(str(vigenere), 'HELLO')
        self.assertEqual(vigenere.cipher_text, 'RIJVS')

        with self.assertRaises(TypeError):
            VigenereCipher(123, 'KEY')
        with self.assertRaises(TypeError):
            VigenereCipher('HELLO', 123)

    def test_custom_mapping_cipher(self):
        my_map = CustomMappingCipher('Hello Students. Welcome to GVSU!')
        self.assertEqual(str(my_map), 'Hello Students. Welcome to GVSU!')
        self.assertEqual(my_map.cipher_text, 'gkPP"m5oK&k$o~*m+kP/"Vkmo"my15YQ')

        with self.assertRaises(TypeError):
            CustomMappingCipher(123)


