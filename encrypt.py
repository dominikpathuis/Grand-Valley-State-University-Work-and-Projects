"""
This is a project for implementing 7 different encryption techniques that are done to modify the data/text.

Name: Dominik Pathuis

Date: 9/23/2024

Version: Python 3.9
"""


class Salting:

    def __init__(self, text: str, salt: str) -> None:
        """
        Constructor method for taking in the text and salt parameters
        :param
        text: The string input that is going to undergo the Salting cipher
        :param
        salt: The string input that will be added to the end of text
        """
        # Ensure that both text and salt come in as strings, and raises a TypeError if they aren't.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')
        if not isinstance(salt, str):
            raise TypeError('Salt must be a string')

        self.salt = salt
        # The ciphered text is stored here
        self.cipher_text = self.salt_cipher(text, salt)

    def salt_cipher(self, text: str, salt: str) -> str:
        """
        Method that creates the salting cipher
        :param
        text: The string input that is going to undergo the salting cipher
        :param
        salt: The string input that will be added to the end of text
        :return:
        The salted text that is then stored in self.cipher_text
        """

        self.cipher_text = text + '' + salt

        return self.cipher_text

    def unsalted_cipher(self, cipher_text: str) -> str:
        """
        Method that decrypts the salting cypher
        :param
        cipher_text: The salted string
        :return:
        The decrypted version of the string
        """
        return cipher_text[: -len(self.salt)]

    def __str__(self) -> str:
        """
        Built-in python method to return a decrypted string
        :return:
        The decrypted text
        """
        return self.unsalted_cipher(self.cipher_text)


class ReverseCipher1:
    def __init__(self, text: str) -> None:
        """
        Constructor method that takes in the text parameter
        :param
        text: The string input that will undergo the 1st reversing cipher
        """
        # Ensures that the text parameter comes in as a string, and raises a TypeError if it doesn't.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')

        # The ciphered text is stored here
        self.cipher_text = self.reversed_text(text)

    def reversed_text(self, text: str) -> str:
        """
        Method to cipher the text accordingly
        :param
        text: The string input that is undergoing the reverse cipher
        :return:
        The encrypted text
        """
        reversed_string = ''

        # Reverse the text character by character
        for i in text:
            reversed_string = i + reversed_string

        return reversed_string

    def __str__(self) -> str:
        """
        Built-in python method to return a decrypted string
        :return:
        The decrypted text
        """
        return self.reversed_text(self.cipher_text)


class ReverseCipher2:
    def __init__(self, text: str) -> None:
        """
        Constructor method that takes in the text parameter
        :param
        text: The string input that will undergo the 2nd reversing cipher
        """
        # Ensures that the text parameter comes in as a string, and raises a TypeError if it doesn't.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')

        # The ciphered text is stored here
        self.cipher_text = self.reversed_text_2(text)

    def reversed_text_2(self, text: str) -> str:
        """
        Method to cipher the text accordingly
        :param
        text: The string input that is undergoing the reverse cipher
        :return:
        The encrypted text
        """
        words = text.split()
        reversed_words = []

        # Reverse each word in the text
        for word in words:
            reversed_word = ''
            # Reverse each character in the word
            for i in word:
                reversed_word = i + reversed_word
            reversed_words.append(reversed_word)

        return ' '.join(reversed_words)

    def __str__(self) -> str:
        """
        Built-in python method to return a decrypted string
        :return:
        The decrypted text
        """
        return self.reversed_text_2(self.cipher_text)


class XORCipher:
    def __init__(self, text: str, key: str) -> None:
        """
        Constructor method that takes in the text and key parameters
        :param
        text: The string input that is undergoing the xor cipher
        :param
        key: The string input to determine how the text will be encrypted
        """
        # Ensures that the text and key parameters come in as a string, and raises a TypeError if they don't.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self.key = key
        # The ciphered text is stored here
        self.cipher_text = self.xor_words(text, key)

    def xor_words(self, text: str, key: str) -> str:
        """
        Method to cipher the text accordingly
        :param
        text: The string input that is undergoing the xor cipher
        :param
        key: The string input that determines how the text will be encrypted
        :return:
        The encrypted text
        """
        xor_list = []

        # Loop over each element in "text" and perform XOR operation with key character
        for i in range(len(text)):
            xor_char = ord(text[i]) ^ ord(key[i % len(key)])
            xor_char = chr(xor_char)
            xor_list.append(xor_char)

        return ''.join(xor_list)

    def __str__(self) -> str:
        """
        Built-in python method to return a decrypted string
        :return:
        The decrypted text
        """
        return self.xor_words(self.cipher_text, self.key)


class CaesarCipher:
    def __init__(self, text: str, key: int) -> None:
        """
        Constructor method that takes in the text and key parameters
        :param
        text: The string input that is undergoing the caesar cipher
        :param
        key: The integer input that determines how to text will be encrypted
        """
        # Ensures that the text and key parameters come in as a string, and int, and raises a TypeError if they are not.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')
        if not isinstance(key, int):
            raise TypeError('Key must be an int')

        self.key = key
        # The ciphered text is stored here
        self.cipher_text = self.caesar_cipher(text, key)

    def caesar_cipher(self, text: str, key: int) -> str:
        """
        Method to cipher the text accordingly using Caesar cipher technique
        :param
        text: The string input that is undergoing the Caesar cipher
        :param
        key: The integer input that determines the character shifts
        :return:
        The encrypted text after applying the Caesar cipher
        """
        ciphered_text = ''

        # Shift each character in the text by the key
        for i in text:
            if i.isupper():
                ciphered_text += chr((ord(i) - ord('A') + key) % 26 + ord('A'))
            elif i.islower():
                ciphered_text += chr((ord(i) - ord('a') + key) % 26 + ord('a'))
            else:
                ciphered_text += i

        return ciphered_text

    def __str__(self) -> str:
        """
        Built-in python method to return a decrypted string
        :return:
        The decrypted text after applying the reverse of the Caesar cipher
        """
        return self.caesar_cipher(self.cipher_text, -self.key)


class VigenereCipher:
    def __init__(self, text: str, key: str) -> None:
        """
        Constructor method that takes in the text and key parameters
        :param
        text: The string input that is going to undergo the Vigenere cipher
        :param
        key: The string input used as the keyword to shift the letters
        """
        # Ensures that both text and key are strings, raising a TypeError if they are not.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')
        if not isinstance(key, str):
            raise TypeError('Key must be a string')

        self.key = key
        # The ciphered text is stored here
        self.cipher_text = self.vigenere_text(text, key)

    def vigenere_text(self, text: str, key: str) -> str:
        """
        Method to cipher the text using Vigenere cipher technique
        :param
        text: The string input that is undergoing the Vigenere cipher
        :param
        key: The string input used to determine the shifts for the Vigenere cipher
        :return:
        The encrypted text after applying the Vigenere cipher
        """

        ciphered_text = ''
        key_length = len(key)

        # Shift each character based on the key
        for i in range(len(text)):
            char = text[i]
            key_char = key[i % key_length]

            if key_char.isdigit():
                shift = int(key_char)
            else:
                shift = ord(key_char.lower()) - ord('a')

            if char.isupper():
                ciphered_text += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            elif char.islower():
                ciphered_text += chr((ord(char) - ord('a') + shift) % 26 + ord('a'))
            else:
                ciphered_text += char

        return ciphered_text

    def decrypt_vigenere(self, cipher_text: str, key: str) -> str:
        """
        Method to decrypt the Vigenere cipher
        :param
        cipher_text: The string input that is going to be decrypted
        :param
        key: The string input used to decrypt the ciphered text
        :return:
        The decrypted text after reversing the Vigenere cipher
        """
        decrypted_text = ''
        key_length = len(key)

        # Reverse the shift for each character based on the key
        for i in range(len(cipher_text)):
            char = cipher_text[i]
            key_char = key[i % key_length]

            if key_char.isdigit():
                shift = int(key_char)
            else:
                shift = ord(key_char.lower()) - ord('a')

            if char.isupper():
                decrypted_text += chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            elif char.islower():
                decrypted_text += chr((ord(char) - ord('a') - shift) % 26 + ord('a'))
            else:
                decrypted_text += char

        return decrypted_text

    def __str__(self) -> str:
        """
        Built-in python method to return the decrypted string
        :return:
        The decrypted text
        """
        return self.decrypt_vigenere(self.cipher_text, self.key)


class CustomMappingCipher:
    def __init__(self, text: str) -> None:
        """
        Constructor method that takes in the text parameter
        :param
        text: The string input that is going to undergo the Custom Mapping cipher
        """
        # Ensures that the text parameter is a string, and raises a TypeError if it is not.
        if not isinstance(text, str):
            raise TypeError('Text must be a string')

        # Custom character map for encryption
        self.character_map = {
            'a': ',', 'b': 'c', 'c': '/', 'd': '&', 'e': 'k', 'f': '}', 'g': '4', 'h': 'w',
            'i': '>', 'j': 'b', 'k': 'W', 'l': 'P', 'm': 'V', 'n': '$', 'o': '"', 'p': '`',
            'q': 'U', 'r': 'x', 's': '~', 't': 'o', 'u': 'K', 'v': 'B', 'w': ']', 'x': 'e',
            'y': '[', 'z': '7', 'A': 'H', 'B': 'i', 'C': 'G', 'D': 's', 'E': ';', 'F': 'A',
            'G': 'y', 'H': 'g', 'I': 'r', 'J': '%', 'K': 'p', 'L': '^', 'M': 'C', 'N': '6',
            'O': 'O', 'P': '8', 'Q': '3', 'R': '\\', 'S': '5', 'T': '0', 'U': 'Y', 'V': '1',
            'W': '+', 'X': '{', 'Y': '2', 'Z': 'D', '0': '(', '1': '=', '2': '?', '3': 'q',
            '4': '<', '5': 't', '6': 'f', '7': 'L', '8': '|', '9': 'l', '!': 'Q', '"': 'F',
            '#': 'h', '$': ')', '%': 'X', '&': 'd', "'": 'j', '(': '.', ')': 'v', '*': 'E',
            '+': "'", ',': '#', '-': '@', '.': '*', '/': 'z', ':': 'S', ';': ':', '<': 'N',
            '=': 'Z', '>': ' ', '?': 'T', '@': '-', '[': 'R', '\\': 'u', ']': 'M', '^': '9',
            '_': '_', '`': 'a', '{': 'n', '|': 'I', '}': 'J', '~': '!', ' ': 'm'
        }

        # Reverse character map for decryption
        self.reverse_character_map = {}
        for key, value in self.character_map.items():
            self.reverse_character_map[value] = key

        # The ciphered text is stored here
        self.cipher_text = self.map_encryption(text)

    def map_encryption(self, text) -> str:
        """
        Method to cipher the text using the custom mapping technique
        :param
        text: The string input that is undergoing the custom mapping cipher
        :return:
        The encrypted text after applying the custom mapping cipher
        """
        encrypted_text = ''

        # Apply the custom character mapping
        for i in text:
            encrypted_text += self.character_map.get(i)
        return encrypted_text

    def map_decryption(self, cipher_text: str) -> str:
        """
        Method to decrypt the custom mapping cipher
        :param
        cipher_text: The string input that is going to be decrypted
        :return:
        The decrypted text after reversing the custom mapping cipher
        """
        decrypted_text = ''

        # Reverse the custom character mapping
        for i in cipher_text:
            decrypted_text += self.reverse_character_map.get(i)
        return decrypted_text

    def __str__(self) -> str:
        """
        Built-in python method to return the decrypted string
        :return:
        The decrypted text
        """
        return self.map_decryption(self.cipher_text)


if __name__ == '__main__':
    text = 'Hello, Students'
    salt = 'gvsulakers'
    key = 'gvsu'
    my_salt = Salting(text, salt)
    rev1 = ReverseCipher1(text)
    rev2 = ReverseCipher2(text)
    xor1 = XORCipher(text, key)
    caesar = CaesarCipher(text, key)
    vigenere = VigenereCipher(text, key)
    my_map = CustomMappingCipher(text)
    print(my_salt)
    print(rev1)
    print(rev2)
    print(xor1)
    print(caesar)
    print(vigenere)
    print(my_map)
