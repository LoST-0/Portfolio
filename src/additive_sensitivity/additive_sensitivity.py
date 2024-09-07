
import numpy as np
from src.utils import generate_binary_strings_recursive, count_equal_letter_run
from src.burrows_wheeler.burrows_wheeler_transform import  BWT

'''
    "Sensitivity of string compressors and repetitiveness measures"
    Tooru Akagia , Mitsuru Funakoshia, Shunsuke Inenaga,
'''

class ADSMeasure:
    """
    A class for measuring the additive sensitivity of the Burrows-Wheeler Transform (BWT)
    with respect to a specific morphing function applied to binary strings.

    The morphing function transforms binary strings by replacing each 'a' with "aab" and each 'b' with "bb".
    This class computes the additive sensitivity of the BWT by comparing the number of equal-letter runs
    in the BWT of the original and morphing-transformed strings.

    Attributes:
        alphabet (list): The alphabet used for morphing. Defaults to ["a", "b"].
    """

    def __init__(self):
        self.alphabet= ["a","b"]

    def __mu(self,letter:str) -> str :
        """
        Transforms a single binary letter to a string based on a predefined mapping.

        Args:
            letter (str): A single binary letter ('0' or '1').

        Returns:
            str: The transformed string ("aab" for '0', "bb" for '1').

        Raises:
            AssertionError: If the letter is not in the alphabet.
        """

        assert letter in  self.alphabet, f"{letter} is not in {self.alphabet}"
        if letter == "a":
            return "aab"
        else:
            return  "bb"

    def  morph(self, text:str) -> str:
        """
        Transforms an entire binary string by applying the morphing function to each character.

        Args:
            text (str): A string composed of binary characters ('a' and 'b').

        Returns:
            str: The morphing-transformed string.
        """
        return ''.join(map(lambda letter:self.__mu(letter), text))

    def __to_proper_alphabet(self,letter:str) -> str:
         """
         Converts a binary character ('0' or '1') to the corresponding character in the alphabet.

         Args:
            letter (str): A binary character ('0' or '1').

         Returns:
            str: The corresponding character from the alphabet ("a" for '0', "b" for '1').
         """
         if letter == "0":
             return self.alphabet[0]
         elif letter == "1":
             return self.alphabet[1]

    def __convert_strings(self,text:str) -> str:
        """
        Converts a binary string ('0's and '1's) to a string of alphabet characters.

        Args:
            text (str): A string of binary characters ('0' and '1').

        Returns:
            str: The string converted to alphabet characters.
        """
        return ''.join([ self.__to_proper_alphabet(letter) for letter in text ])


    def additive_sensitivity(self, order:int) -> int:
        """
        Computes the additive sensitivity of the BWT with respect to the morphing function.

        The sensitivity is measured by computing the maximum difference (infinity norm)
        between the number of equal-letter runs in the BWT of original binary strings and
        their morphing-transformed versions.

        Args:
            order (int): The length of binary strings to generate.

        Returns:
            int: The additive sensitivity of the BWT.
        """
        bwt = BWT()
        strings = generate_binary_strings_recursive(order)
        strings = list(map(lambda string:self.__convert_strings(string), strings))
        morphed_strings =list(map(lambda string:self.morph(string), strings))
        # Get the transform
        bwt_strings  = [ bwt.linear_transform(text)[0] for text in strings ]
        bwt_morphed_strings = [bwt.linear_transform(text)[0] for text in morphed_strings]
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
