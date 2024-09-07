
from src.burrows_wheeler.sais import sais_construction


class BWT:
  """
    A class to perform the Burrows-Wheeler Transform (BWT) and its inverse.

    The BWT is a data transformation algorithm that rearranges a string into runs of similar characters.
    It is useful for data compression and is a fundamental component of the bzip2 compressor.

    Methods:
        transform(text): Perform the standard BWT on the given text.
        reverse_transform(L, I): Reverse the BWT to recover the original text.
        linear_transform(text): Perform the BWT using the SA-IS algorithm for linear time complexity.
  """
  def __init__(self) -> None:
    pass

  @staticmethod
  def __get_cyclic_rotations(text) -> list:
    """
      Generate all cyclic rotations of the input text.

      :param text: The input string to rotate.
      :return: A list of all cyclic rotations of the input text.
      :rtype: list
    """
    return [text[x:]+text[:x] for x in range(len(text))]

  @staticmethod
  def fl_mapping(L):
    """
      Create a forward mapping from the last column (L) to the first column (F) of the BWT matrix.

      :param L: The last column of the BWT matrix.
      :return: A tuple containing the mapping from L to F and the sorted first column F.
      :rtype: tuple
    """
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
    """
      Reverse the BWT to recover the original text.

      :param L: The last column of the BWT matrix.
      :param I: The index of the original text in the sorted list of cyclic rotations.
      :return: The original string before transformation.
      :rtype: str
    """
    w = ''
    tau,F = self.fl_mapping(L)
    mapped = tau[I]

    for _ in range(0,len(L)):
      w = F[mapped] + w
      mapped = tau[mapped]
    return w
       
  def transform(self,text):
    """
      Perform the Burrows-Wheeler Transform (BWT) on the input text.

      :param text: The input string to transform.
      :return: A tuple containing the last column of the BWT matrix and the index of the original string.
      :rtype: tuple
    """
    rotations = self.__get_cyclic_rotations(text)
    # Sort the cyclic rotations
    rotations.sort(reverse=False)
    # Get the index of the original text
    I = rotations.index(text)
    # Get the Last column of the conceptual Matrix MT
    L = ''.join([
      w[-1] for w in rotations
    ])

    return L,I

  @staticmethod
  def sais_transform(text,suffix_array):
      """
      Perform the Burrows-Wheeler Transform (BWT) using the suffix array.

      :param text: The input string to transform.
      :param suffix_array: The suffix array of the input string.
      :return: A tuple containing the last column of the BWT matrix and the index of the original string.
      :rtype: tuple
      """
      # Use the suffix array instead of the cyclic rotations
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
      """
      Perform the Burrows-Wheeler Transform (BWT) in linear time using the SA-IS algorithm.

      :param text: The input string to transform.
      :return: A tuple containing the last column of the BWT matrix and the index of the original string.
      :rtype: tuple
      """
      # Wrapper around sais_construction
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
