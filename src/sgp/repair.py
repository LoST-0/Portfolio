

import string
from collections import defaultdict, deque
from src.utils import *

NON_TERMINALS = list(string.ascii_uppercase + string.digits)


class RePairCompression:
    """
    A class implementing the RePair compression algorithm.

    This algorithm compresses text by repeatedly replacing the most frequent pairs of characters
    with non-terminals until no more frequent pairs can be found.

    Attributes:
        non_terminal_counter (int): Counter for generating non-terminal symbols.
    """
    def __init__(self):
        """
        Initializes the RePairCompression class.
        """
        self.non_terminal_counter = 0

    @staticmethod
    def __get_next_non_terminal():
        """
        Generates and returns the next non-terminal symbol from the predefined list of non-terminals.

        Returns:
            str: The next non-terminal symbol.
        """
        return NON_TERMINALS.pop()
    @staticmethod
    def __scan_text(text):
        """
        Scans the text to find all pairs of consecutive characters and their frequencies.

        Args:
            text (list): The text to scan, represented as a list of characters.

        Returns:
            tuple: A tuple containing:
                - pairs (defaultdict(int)): A dictionary with pairs of characters as keys and their frequencies as values.
                - pair_indices (defaultdict(list)): A dictionary with pairs of characters as keys and lists of indices where these pairs occur as values.
        """
        pairs = defaultdict(int)
        pair_indices = defaultdict(list)

        for i in range(0,len(text) - 2,2):
            pair = text[i:i + 2]
            pair = ''.join(pair)
            pairs[pair] += 1
            pair_indices[pair].append(i)

        return pairs, pair_indices
    @staticmethod
    def __get_most_frequent(pairs):
        """
        Finds the most frequent pair of characters from the dictionary of pairs.

        Args:
            pairs (defaultdict(int)): A dictionary with pairs of characters as keys and their frequencies as values.

        Returns:
            tuple: A tuple containing:
                - str: The most frequent pair of characters.
                - int: The frequency of the most frequent pair.
        """
        most_frequent = max(pairs.items(), key=lambda x: x[1])
        return most_frequent[0], pairs[most_frequent[0]]

    def build_grammar(self, text):
        """
        Builds a grammar for the text using the RePair compression algorithm.

        Args:
            text (str): The text to compress.

        Returns:
            tuple: A tuple containing:
                - grammar (dict): A dictionary with non-terminals as keys and the corresponding replacements as values.
                - str: The compressed text using non-terminals.
        """
        grammar = {}
        text = list(text)

        while True:
            pairs, pair_indices = self.__scan_text(text)

            if not pairs:
                break

            most_frequent_pair, frequency = self.__get_most_frequent(pairs)

            if frequency <= 1:
                break

            non_terminal = self.__get_next_non_terminal()
            grammar[non_terminal] = most_frequent_pair

            indices = pair_indices[most_frequent_pair]
            i = 0

            while i < len(indices):
                index = indices[i]

                if index < len(text) - 1 and text[index] + text[index + 1] == most_frequent_pair:
                    text[index] = non_terminal
                    # you are reducing the overall size of text
                    del text[index + 1]
                    
                    if i + 1 < len(indices) and indices[i + 1] == index + 1:
                        indices.pop(i + 1)
                    # Reduce by one the index position
                    indices = [x - 1 if x > index else x for x in indices]

                i += 1

        return grammar, ''.join(text)

    @staticmethod
    def decompress(grammar, ctext):
        """
        Decompresses the compressed text using the grammar.

        Args:
            grammar (dict): A dictionary with non-terminals as keys and the corresponding replacements as values.
            ctext (str): The compressed text using non-terminals.

        Returns:
            str: The decompressed text.
        """
        text = deque(ctext)
        result = []
        while text:
            c = text.popleft()
            if c in grammar:
                expansion = grammar[c]
                text.extendleft(reversed(expansion))
            else:
                result.append(c)

        return ''.join(result)

    @staticmethod
    def grammar_size(grammar):
      """
        Calculates the size of the grammar based on the length of the replacements.

        Args:
            grammar (dict): A dictionary with non-terminals as keys and the corresponding replacements as values.

        Returns:
            int: The size of the grammar.
      """
      size = 0
      for expansion in  grammar.values():
        size += len(expansion)
        
      return size

class RePairCNFCompression(RePairCompression):
  """
    A class extending RePairCompression to include conversion to Chomsky Normal Form (CNF).

    This class builds a grammar in CNF where each production rule is of the form:
    - A -> BC
    - A -> a
    where A, B, and C are non-terminals and a is a terminal.

    Methods:
        __trivial_pairing(ctext, S): Creates trivial pairings for CNF conversion.
        __substitute_all_terminals(text): Substitutes all terminal symbols with non-terminals.
  """
  
  def __init__(self):
      super().__init__()

  @staticmethod
  def __trivial_pairing(ctext:str,S):
    """
      Creates trivial pairings for CNF conversion by replacing each sequance of characters, with a new non-terminal.
      A -> BCD  becomes    A -> BY
                           Y -> CD

      Args:
          ctext (str): The compressed text.
          S (str): The starting non-terminal symbol for CNF conversion.

      Returns:
          dict: A dictionary with non-terminals as keys and the corresponding replacements as values.
    """
    fgrammar = {}

    for index,nterminal in enumerate(ctext):

      if index == len(ctext) - 1:
        aux_nterminal = ""
      else:
       aux_nterminal = NON_TERMINALS.pop()

      fgrammar[S] = nterminal + aux_nterminal

      S = aux_nterminal
    return fgrammar
      
      
      
  def build_grammar(self, text):
      """
      Builds a grammar for the text using the RePair compression algorithm and converts it to CNF.

      Args:
          text (str): The text to compress.

      Returns:
          tuple: A tuple containing:
              - grammar (dict): A dictionary with non-terminals as keys and the corresponding replacements as values.
              - str: The CNF compressed text.
      """
     
      text,bgrammar = self.__substitute_all_terminals(text)
      grammar, ctext = super().build_grammar(text)
      bgrammar.update(grammar)

      A = NON_TERMINALS.pop(0)

      grammar = self.__trivial_pairing(ctext,A)
      grammar.update(bgrammar)

      return grammar, grammar[A]

  @staticmethod
  def __substitute_all_terminals(text:str) -> tuple[str,dict]:
    """
     Substitutes all terminal symbols with non-terminals and creates a grammar for these substitutions.

      Args:
          text (str): The text with terminal symbols.

      Returns:
          tuple: A tuple containing:
              - str: The modified text with terminal symbols substituted.
              - dict: A dictionary with terminals as keys and non-terminals as values.
    """
    text = text.upper()
    uniques = list(set(text))
    for c in uniques:
      NON_TERMINALS.remove(c)
    grammar = {unique:unique.lower() for unique in uniques}
    
    return text,grammar
      
def testcase(r:RePairCompression,text:str):

    grammar, ctext = r.build_grammar(text)
    print(f"Using compressor: {r.__class__} ")
    print(f"Compressed text: {ctext}")
    print(f"Grammar size: {r.grammar_size(grammar)}")
    print(f"Decompressed text: {r.decompress(grammar, ctext)}")
    print("---- Grammmar ----")
    for head,tail in grammar.items():
      print(f"{head} -> {tail}")

    print("------------------")
    
    return


def main():
  r1 = RePairCompression()
  r2 = RePairCNFCompression()
  text = generate_random_text(alphabet=["a","b","c"],run_equal=3,len_text=20)
  testcase(r1,text)
  testcase(r2,text)
  

if __name__ == "__main__":
  main()