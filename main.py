import pandas as pd
import re
import os
import json

from math import ceil
from threading import Thread


class ThreadsNumberError(Exception):
    def __init__(self):            
        # Call the base class constructor with the parameters it needs
        super().__init__('Threds number must be 1 or greater')


class Decrypter:
    def __init__(self, words='polish_words', alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ', threads_number=1):
        self.words = pd.read_csv(words)[:50]
        self.alphabet = alphabet.upper()
        self.threads_number = threads_number
        self.threshold = self.words.shape[0] // threads_number   
        
        if self.threads_number < 1:
            raise ThreadsNumberError
        
    def decrypt(self, message): 
        message = message.upper()
        
        def decrypt_msg(message, words_set):
            min_words = ceil(len(message) / 50)
            print(min_words)
            
            for word in words_set:
                result = '' 
                words_counter = 0
                sentence = word+self.alphabet
                coded_alphabet = ''.join([char for i, char in enumerate(sentence) if char not in sentence[:i]])
                
                # for char in message:
                #     index = coded_alphabet.index(char)
                #     result += self.alphabet[index]
                    
                result = message

                for check_word in self.words['word']:

                    if check_word in result:
                        words_counter += len(re.findall(check_word, result))
                        
                    if words_counter == min_words:                        
                        if not os.path.isfile('results.json'):
                            with open('results.json', 'w') as file:
                                json.dump({'results': []}, file)
                        
                        with open('results.json', 'r') as file:
                            data = json.load(file)
                            data['results'].append({
                                'alphabet': coded_alphabet,
                                'message': result
                            })
                            
                        break
                    

        for i in range(self.threads_number):
            thread = Thread(target=decrypt_msg, args=(message, [self.words['word'][i*self.threshold:self.threshold + i*self.threshold]]))
            thread.start()      
                
    
decrypter = Decrypter()

# decrypter.decrypt('ABACJA')


