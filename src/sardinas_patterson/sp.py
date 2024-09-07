

class Codex:
    """
    A class to represent a codebook mapping.

    :param codebook: A dictionary representing the codebook, where keys are symbols and values are codewords.
    :type codebook: dict, optional
    """
    def __init__(self, codebook=None):
        if codebook is None:
            codebook = {}
        self.mapping = codebook

    def __str__(self):
        return str(self.mapping)


class SPChecker:
    """
    A class to check if a codebook is uniquely decodable (UD) by using suffix-prefix properties.

    Attributes:
        codewords: A set of all codewords in the codebook.
        pairings: A list of pairings of codewords used in factorization.
        seen: A list of previously seen sets of suffixes during the check process.
    """
    def __init__(self) -> None:
        self.codewords = None
        self.pairings = []
        self.seen = []
        
    def __flush(self):
        """
        Resets the attributes to their initial states.
        """
        self.codewords = None
        self.pairings = []
        self.seen = []

    def find_factorizations(self, remaining_path, current_factorization):
          """
            Recursively finds all possible factorizations of the remaining path.

           :param remaining_path: The remaining portion of the string to factorize.
           :param current_factorization: The current factorization list being built.
           :return: A list of all possible factorizations.
           :rtype: list
          """
          if not remaining_path:
                return [current_factorization]

          factorizations = []
          for cw in self.codewords:
                if remaining_path.startswith(cw):
                    new_factorization = current_factorization + [cw]
                    factorizations += self.find_factorizations(
                        remaining_path[len(cw):], new_factorization)
          return factorizations

    def __factorize(self, path):
      """
        Finds two different factorizations of the given path, if they exist.

        :param path: The path (string) to factorize.
        :return: A tuple of two different factorizations as strings. If less than two factorizations exist, returns empty strings.
        :rtype: tuple
      """
      if not path:
        return None

      all_factorizations = self.find_factorizations(path, [])
    
      if len(all_factorizations) < 2:
          return '', ''

      s1 = ' '.join(all_factorizations[0])
      s2 = ' '.join(all_factorizations[1])

      return s1, s2

      
    def next_suffix_set(self, S_i):
        """
        Computes the next set of suffixes in the UD check process.

        :param S_i: The current set of suffixes.
        :return: The next set of suffixes.
        :rtype: set
        """
        S_i_plus_1 = set()
        pairs = set()

        for a in self.codewords:
            for b in S_i:
                if a.startswith(b) and a != b:
                    S_i_plus_1.add(a[len(b):])
                    pairs.add((a, b, a[len(b):]))

                elif b.startswith(a) and a != b:
                    S_i_plus_1.add(b[len(a):])
                    pairs.add((b, a, b[len(a):]))

        self.pairings.append(pairs)
        return S_i_plus_1


    @staticmethod
    def __get_pair_index(pairing,cw):
      """
        Finds the index of a codeword in a pairing list.

        :param pairing: The list of pairings.
        :param cw: The codeword to find.
        :return: The index and the corresponding pair as a tuple. If not found, returns (None, None).
        :rtype: tuple
      """
      for index,(x,y,w) in enumerate(pairing):
        if cw == w:
          return index,(x,y,w)
      else:
        return None,None
      
          
    
    def _get_not_unique_decomposition(self,cw):
      """
        Finds a non-unique decomposition for a given codeword.

        :param cw: The codeword to decompose.
        :return: A tuple of two different factorizations as strings.
        :rtype: tuple
       """
      self.pairings.reverse()
      cws = cw.pop()      
      s = ''
      yi = ''
      cwsp = ''
      
      for pairing in self.pairings:
        
        index,pair = self.__get_pair_index(pairing,cws)
        if index is None:
          #Try the other way
          index,pair = self.__get_pair_index(pairing,yi+cwsp)

        if index is not None:  
          _,yi,_ = pair
          s  = cws + s
          cwsp = cws
          cws = yi
      
      s = cws + s
      return  self.__factorize(s)

          
    def is_ud(self, code: Codex):
        """
        Checks if the given code is uniquely decodable (UD).

        :param code: The codebook to check, represented as a Codex object.
        :return: A tuple where the first element is a boolean indicating if the code is UD,
                 and the second element is either None (if UD) or a tuple of non-unique decompositions.
        :rtype: tuple
        """
        S_0 = set(code.mapping.values())
        self.codewords = S_0
        S_i = S_0

        while S_i:

            S_i = self.next_suffix_set(S_i)
            S_i.discard('')
            
            if not S_i:
                self.__flush()

                return True, None

            if any(residual in self.codewords for residual in S_i):
                nud_strings = self._get_not_unique_decomposition(S_i & S_0)
                self.__flush()
                return False, nud_strings

            if any(past == S_i for past in self.seen):
                self.__flush()
                return True, None

            self.seen.append(S_i)

        self.__flush()
        return True, None



def main(code:Codex):
    checker = SPChecker()
    is_ud, decompositions = checker.is_ud(code)
    print("Code: {}".format(code))
    print("Is UD: {}".format(is_ud))
    print("Decompositions: {}".format(decompositions))


if __name__ == "__main__":
    cd = Codex( {
    "A": "0",
    "B": "01",
    "C": "011",
    "D": "0111"
     })
    main(cd)