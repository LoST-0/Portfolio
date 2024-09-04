
import numpy as np
from src.utils import generate_binary_strings_recursive, count_equal_letter_run
from src.burrows_wheeler.burrows_wheeler_transform import  BWT

class ADSMeasure:

    def __init__(self):

        self.alphabet= ["a","b"]

    def __mu(self,letter:str) -> str :
        assert letter in  self.alphabet, f"{letter} is not in {self.alphabet}"
        if letter == "a":
            return "aab"
        else:
            return  "bb"

    def  morph(self, text:str) -> str:
        return ''.join(map(lambda letter:self.__mu(letter), text))

    def __to_proper_alphabet(self,letter:str) -> str:
         if letter == "0":
             return self.alphabet[0]
         elif letter == "1":
             return self.alphabet[1]

    def __convert_strings(self,text:str) -> str:
        return ''.join([ self.__to_proper_alphabet(letter) for letter in text ])


    def additive_sensitivity(self, order:int) -> int:
        bwt = BWT()
        strings = generate_binary_strings_recursive(order)
        strings = list(map(lambda string:self.__convert_strings(string), strings))
        morphed_strings =list(map(lambda string:self.morph(string), strings))
        # Get the transform
        bwt_strings  = [ bwt.transform(text)[0] for text in strings ]
        bwt_morphed_strings = [bwt.transform(text)[0] for text in morphed_strings]
        # Get the runs
        rs    = np.array([count_equal_letter_run(text) for text in bwt_strings])
        mu_rs = np.array([count_equal_letter_run(text) for text in bwt_morphed_strings])
        difference    =  mu_rs - rs
        infinity_norm = np.max(difference)
        return infinity_norm


def main():
    ads = ADSMeasure()
    print(ads.additive_sensitivity(order=5))

    return

if __name__ == "__main__":
    main()
