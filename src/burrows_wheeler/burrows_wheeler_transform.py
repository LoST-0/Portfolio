
import pandas as pd
from src.utils import *
from src.burrows_wheeler.sais import sais_construction


class BWT:
  def __init__(self) -> None:
    pass

  @staticmethod
  def __get_cyclic_rotations(text) -> list:
    return [text[x:]+text[:x] for x in range(len(text))]

  @staticmethod
  def fl_mapping(L):
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

  @staticmethod
  def sais_transform(text,suffix_array):

      n = len(suffix_array)
      bwt = []
      for i in range(n):
          suffix_index = suffix_array[i]
          if suffix_index == 0:
              bwt.append("$")
          else:
              bwt.append(text[suffix_index - 1])
      
      return ''.join(bwt), suffix_array.index(0)

  def linear_transform(self,text):
      print(text)
      suffix_array = sais_construction(text)
      return  self.sais_transform(text,suffix_array)



def main():
   bwt = BWT()
   text = "amanaplanacanalpanama"

   L, I = bwt.transform(text)
   w = bwt.reverse_transform(L, I)
   assert  w == text

   L, I = bwt.linear_transform(text)
   w = bwt.reverse_transform(L, I)
   assert w == text + "$"

if __name__ == '__main__':
    main()
