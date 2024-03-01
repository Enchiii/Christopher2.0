import pandas as pd
import re
import numpy as np

from math import ceil
from threading import Thread


class ThreadsNumberError(Exception):
    def __init__(self):
        # Call the base class constructor with the parameters it needs
        super().__init__("Threds number must be 1 or greater and must be integer")


class Decrypter:
    def __init__(
        self,
        words: str = "polish_words",
        alphabet: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        threads_number: int = 1,
        print_results: bool = True,
        results_file_name: str = 'results'
    ):
        self.words = pd.read_csv(words)
        self.alphabet = alphabet.upper()
        self.threads_number = threads_number
        self.threshold = self.words.shape[0] // self.threads_number
        self.possible_results = np.array([])
        self.print_results = print_results
        self.results_file_name = results_file_name

        if self.threads_number < 1 or not (self.threads_number / 1).is_integer():
            raise ThreadsNumberError
            
    @staticmethod
    def remove_special_chars(message: str) -> str:
        special_chars = "!@#$%^&*()_-+=,<.>?/|;:1234567890 "
        for char in special_chars:
            message = message.replace(char, "")

        strange = "ąćęłńóśźż".upper()
        ascii_replacement = "acelnoszz".upper()
        translator = str.maketrans(strange, ascii_replacement)

        return message.upper().translate(translator)

    def decrypt(self, message: str):
        def decrypt_msg(message, words_set, depth: int = 50):
            min_words: int = ceil(len(message) / depth)

            for word in words_set:
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
                        self.possible_results = np.append(self.possible_results, [f"alphabet: {coded_alphabet} message: {result}"])
                        print(coded_alphabet, ' ', result)
                        break

        threads: list = []
        for i in range(self.threads_number):
            thread = Thread(
                target=decrypt_msg,
                args=(
                    message,
                    self.words["word"][
                        i * self.threshold: self.threshold + i * self.threshold
                    ],
                ),
            )
            threads.append(thread)

        for t in threads:
            t.start()

        for t in threads:
            t.join()

        self.possible_results.reshape(len(self.possible_results) // 2, 2)
        df = pd.DataFrame(self.possible_results, columns=["Alphabet", "Message"])
        df.to_csv(f'{self.results_file_name}.csv')

        if self.print_results:
            print(df)

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


decrypter = Decrypter(threads_number=150)

msg = decrypter.remove_special_chars("abacja")
msg = decrypter.encrypt(msg, "abaka")

decrypter.decrypt(msg)
