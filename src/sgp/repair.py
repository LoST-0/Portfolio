

import string
from collections import defaultdict, deque
from src.utils import *

NON_TERMINALS = list(string.ascii_uppercase + string.digits)

class RePairCompression:

    def __init__(self):
        self.non_terminal_counter = 0

    def __get_next_non_terminal(self):
        
        return NON_TERMINALS.pop()

    def __scan_text(self, text):
        pairs = defaultdict(int)
        pair_indices = defaultdict(list)

        for i in range(0,len(text) - 2,2):
            pair = text[i:i + 2]
            pair = ''.join(pair)
            pairs[pair] += 1
            pair_indices[pair].append(i)

        return pairs, pair_indices

    def __get_most_frequent(self, pairs):
        most_frequent = max(pairs.items(), key=lambda x: x[1])
        return most_frequent[0], pairs[most_frequent[0]]

    def build_grammar(self, text):
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
                    del text[index + 1]
                    
                    if i + 1 < len(indices) and indices[i + 1] == index + 1:
                        indices.pop(i + 1)
                    indices = [x - 1 if x > index else x for x in indices]

                i += 1

        return grammar, ''.join(text)

    def decompress(self, grammar, ctext):
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

    def grammar_size(self,grammar):
      size = 0
      for expansion in  grammar.values():
        size += len(expansion)
        
      return size

class RePairCNFCompression(RePairCompression):
  
  def __init__(self):
      super().__init__()
      
  def __trivial_pairing(self,ctext:str,S):
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
     
      text,bgrammar = self.__substitute_all_terminals(text)
      grammar, ctext = super().build_grammar(text)
      bgrammar.update(grammar)
      A = NON_TERMINALS.pop(0)
      grammar = self.__trivial_pairing(ctext,A)
      grammar.update(bgrammar)
      return grammar, grammar[A]
    
  def __substitute_all_terminals(self,text:str) -> tuple[str,dict]:
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