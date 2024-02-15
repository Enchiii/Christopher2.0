import pandas as pd
import re
import os
import json

from math import ceil
from threading import Thread


class ThreadsNumberError(Exception):
    def __init__(self):            
        # Call the base class constructor with the parameters it needs
        super().__init__('Threds number must be 1 or greater and must be integer')


class Decrypter:
    def __init__(self, words: object='polish_words', alphabet: str='ABCDEFGHIJKLMNOPQRSTUVWXYZ', threads_number: int=1):
        self.words = pd.read_csv(words)[:50]
        self.alphabet = alphabet.upper()
        self.threads_number = threads_number
        self.threshold = self.words.shape[0] // self.threads_number   

        if self.threads_number < 1  or not (self.threads_number/1).is_integer():
            raise ThreadsNumberError
        
    def decrypt(self, message: str): 
        message = message.upper()
        
        def decrypt_msg(message: str, words_set: object):
            min_words: int = ceil(len(message) / 50) # minimalna liczba słow ktora musi sie pojawic w wiadomosci aby uznac za rozwiazanie

            for word in words_set:
                result: str = ''
                words_counter: int = 0
                sentence: str = word+self.alphabet
                coded_alphabet: str = ''.join([char for i, char in enumerate(sentence) if char not in sentence[:i]])
                
                for char in message:
                    index = coded_alphabet.index(char)
                    result += self.alphabet[index]

                for check_word in self.words['word']:

                    if check_word in result:
                        words_counter += len(re.findall(check_word, result))
                        
                    if words_counter == min_words:                 
                        if not os.path.isfile('results.json'):
                            with open('results.json', 'w') as file:
                                json.dump({'results': []}, file)
                        
                        with open('results.json') as file:
                            data = json.load(file)
                            data['results'].append({
                                'alphabet': coded_alphabet,
                                'message': result
                            })
                        
                        with open('results.json', 'w') as file:
                            json.dump(data, file)
                            
                        break
                    

        for i in range(self.threads_number):
            thread = Thread(target=decrypt_msg, args=(message, self.words['word'][i*self.threshold : self.threshold + i*self.threshold]))
            thread.start()
    
    def encrypt(self, message: str, key_word: str):
        pass      
                
    
decrypter = Decrypter()

decrypter.decrypt('ABACJA')
