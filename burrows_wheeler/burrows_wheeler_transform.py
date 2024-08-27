
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
from functools import lru_cache

from sais import sais_construction




class BWT:
  def __init__(self) -> None:
    pass
    
  def __get_cyclic_rotations(self,text) -> list:
    return [text[x:]+text[:x] for x in range(len(text))]
  
  def fl_mapping(self,L):
    F = sorted(L)
    fl_map = {}
    count_L = {char: 0 for char in set(L)}
  
    first_occurrence = {}
    for i, char in enumerate(F):
        if char not in first_occurrence:
            first_occurrence[char] = i

    for index, char in enumerate(L):
        fl_index = first_occurrence[char] + count_L[char]
        fl_map[index] = fl_index
        count_L[char] += 1

    return fl_map,F
    
  def reverse_transform(self, L, I):  
    w = ''
    tau,F = self.fl_mapping(L)
    mapped = tau[I]
    
    for _ in range(0,len(L)):
      w += F[mapped]
      mapped = tau[mapped]
    return w[::-1]
       
  def transform(self,text): 
    rotations = self.__get_cyclic_rotations(text)
    rotations.sort(reverse=False)
    I = rotations.index(text)
    L = ''.join([
      w[-1] for w in rotations
    ])

    return L,I
  
  def sais_transform(self,text,suffix_array):
      n = len(text)
      bwt = []
      for i in range(n):
          suffix_index = suffix_array[i]
          if suffix_index == 0:
              bwt.append("$")
          else:
              bwt.append(text[suffix_index - 1])
      
      return ''.join(bwt), np.where(suffix_array == 0)[0][0]

@lru_cache(maxsize=64)
def fibonacci_word(order):
  if order<0:
    return ''
  elif order == 0:
    return "b"
  elif order == 1:
    return "a"
  else:
    return fibonacci_word(order - 1) + fibonacci_word(order - 2)
    

def count_equal_letter_run(text):
    if not text:
        return 0

    run_count = 1
    current_char = text[0]

    for char in text[1:]:
        if char != current_char:
            run_count += 1
            current_char = char

    return run_count



def run_test(text, bwt):
    print("-" * 20)
    print("Running test sample: ", text)

    # Run BWT and inverse BWT
    L, I = bwt.transform(text)
    w = bwt.reverse_transform(L, I)

    print(f"BWT({text}): ", L)
    print(f"IBWT({L}): ", w)
    assert w == text, "Ops! The inverse BWT did not match the original text."

    r = count_equal_letter_run(L)

    print("SAIS-Test")
    # Construct the suffix array
    suffix_array = sais_construction(text)

    print(f"Suffix Array: {suffix_array}")

    # Run BWT using SA-IS
    L, I = bwt.sais_transform(text, suffix_array)
    w = bwt.reverse_transform(L, I)

    print(f"SAIS-BWT({text}$): ", L)
    print(f"SAIS-IBWT({L}): ", w)

    rs = count_equal_letter_run(L)

    return r, rs


def main():
    order = 4
    bwt = BWT()
    testcases = [
        fibonacci_word(order),
        fibonacci_word(order * 2),
        fibonacci_word(order * 3),
        fibonacci_word(order)[:-1],
        fibonacci_word(order * 2)[:-1],
        fibonacci_word(order * 3)[:-1],
    ]

    runs = []
    for text in testcases:
        r, rs = run_test(text, bwt)
        runs.append((r, rs))

    # Create a pandas DataFrame for better visualization and manipulation
    df = pd.DataFrame(
        runs, columns=["Run BWT(T)", "Run BWT(T$)"], index=testcases)

    print("-" * 20)
    print("Results:")
    print(df)
    
    df.plot(kind='bar', figsize=(10, 6))

    plt.title('BWT and SAIS-BWT Runs')
    plt.xlabel('Fibonacci Words')
    plt.ylabel('Number of Runs')
    plt.xticks(rotation=45)
    
    plt.show()


if __name__ == '__main__':
    main()
