import pandas as pd

from threading import Thread

class Decrypter:
    def __init__(self, words='polish_words', alphabet='ABCDEFGHIJKLMNOPQRSTUVWXYZ', threads_number=1):
        self.words = pd.read_csv(words)
        self.alphabet = alphabet.upper()
        self.threads_number = threads_number    
        
    def decrypt(self, message): 
        message = message.upper()
        
        def decrypt_msg(words_set):
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
                        words_counter += 1
                        
                    if words_counter == 1: # zmienic w zaleznosci od dlugosci wiadomosci
                        # zatrzymac wszystkie thready jesli sie da i dodac alfabet i odzszyfrowana wiadomosc do pliku z wynikami
                        return 
                    

        for i in range(self.threads_number):
            thread = Thread(target=decrypt_msg, args=([self.words['word'][:1]])) #IMPORTANT it is setting for only first 5 words rn
            thread.start()      
                
    
decrypter = Decrypter()

decrypter.decrypt('ABACJA')
