import pandas as pd
import re
import os
import json

from math import ceil
from threading import Thread


class Decrypter:
    def __init__(
        self,
        words: str = "polish_words",
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    ):
        self.words = pd.read_csv(words)
        self.alphabet = alphabet.upper()

    @staticmethod
    def remove_special_chars(message: str) -> str:
        special_chars = "!@#$%^&*()_-+=,<.>?/|;:1234567890 "
        for char in special_chars:
            message = message.replace(char, "")

        strange = "ąćęłńóśźż".upper()
        ascii_replacement = "acelnoszz".upper()
        translator = str.maketrans(strange, ascii_replacement)

        return message.upper().translate(translator)

    def decrypt(self, message: str, depth: int = 50):
        min_words: int = ceil(len(message) / depth)

        for word in self.words["word"]:
            result: str = ""
            words_counter: int = 0
            sentence: str = word + self.alphabet
            coded_alphabet: str = "".join(
                [
                    char
                    for i, char in enumerate(sentence)
                    if char not in sentence[:i]
                ]
            )

            for char in message:
                index: int = coded_alphabet.index(char)
                result += self.alphabet[index]

            for check_word in self.words["word"]:

                if check_word in result:
                    words_counter += len(re.findall(check_word, result))

                if words_counter == min_words:
                    if not os.path.isfile("results.json"):
                        with open("results.json", "w") as file:
                            json.dump({"results": []}, file)

                    with open("results.json") as file:
                        data = json.load(file)
                        data["results"].append(
                            {"alphabet": coded_alphabet, "message": result}
                        )

                    with open("results.json", "w") as file:
                        json.dump(data, file)

                    break

    def encrypt(self, message: str, key_word: str) -> str:
        key_word = key_word.upper()
        result: str = ""
        sentence: str = key_word + self.alphabet
        coded_alphabet: str = "".join(
            [char for i, char in enumerate(sentence) if char not in sentence[:i]]
        )

        for char in message:
            index: int = self.alphabet.index(char)
            result += coded_alphabet[index]

        return result


decrypter = Decrypter()

msg = decrypter.remove_special_chars("abacja???@2")
msg = decrypter.encrypt(msg, "abaka")

decrypter.decrypt(msg)
