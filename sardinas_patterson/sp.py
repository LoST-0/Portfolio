import json
import argparse
import os



class Codex:
    def __init__(self, codebook={}):
        self.mapping = codebook

    def __str__(self):
        return str(self.mapping)


class SPChecker:

    def __init__(self) -> None:
        self.codewords = None
        self.pairings = []
        self.seen = []
        
    def _flush(self):
        self.codewords = None
        self.pairings = []
        self.seen = []


    def find_factorizations(self, remaining_path, current_factorization):
      
          if not remaining_path: 
                return [current_factorization]

          factorizations = []
          for cw in self.codewords:
                if remaining_path.startswith(cw):
                    new_factorization = current_factorization + [cw]
                    factorizations += self.find_factorizations(
                        remaining_path[len(cw):], new_factorization)
          return factorizations

    def _factorize(self, path):
      if not path:
        return None
      all_factorizations = self.find_factorizations(path, [])
    
      if len(all_factorizations) < 2:
          return '', ''
      
        
      s1 = ' '.join(all_factorizations[0])
      s2 = ' '.join(all_factorizations[1])

      return s1, s2


      
      
    def next_suffix_set(self, S_i):
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
        
    def _get_pair_index(self,pairing,cw):
      for index,(x,y,w) in enumerate(pairing):
        if cw == w:
          return index,(x,y,w)
      else:
        return None,None
      
          
    
    def _get_not_unique_decomposition(self,cw):

      self.pairings.reverse()
      cws = cw.pop()      
      s = ''
      yi = ''
      cwsp = ''
      
      for pairing in self.pairings:
        
        index,pair = self._get_pair_index(pairing,cws)
        if index is None:
          #Try the other way
          index,pair = self._get_pair_index(pairing,yi+cwsp)

        if index is not None:  
          _,yi,_ = pair
          s  = cws + s
          cwsp = cws
          cws = yi
      
      s = cws + s
      return  self._factorize(s)
     
      
          
    def isUD(self, code: Codex):
        S_0 = set(code.mapping.values())
        self.codewords = S_0
        S_i = S_0

        while S_i:
            S_i = self.next_suffix_set(S_i)
            S_i.discard('')
            
            if not S_i:
                self._flush()
                return True, None

            if any(residual in self.codewords for residual in S_i):
                nud_strings = self._get_not_unique_decomposition(S_i & S_0)
                self._flush()
                return False, nud_strings

            if any(past == S_i for past in self.seen):
                self._flush()
                return True, None

            self.seen.append(S_i)

        self._flush()
        return True, None


def main(raw_codes):
    checker = SPChecker()

    for code in raw_codes:
        # Create Codex instances
        codex = Codex(raw_codes[code])
        # Check if the code is uniquely decodable
        is_ud, factorization = checker.isUD(codex)
        print("Code:", codex)
        print("Is UD:", is_ud)
        if not is_ud:
            print("Not uniquely decodable. Factorization:", factorization)
            
        print("-"*30)


def parse_input(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")

    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--input', help='Path to input JSON file', required=True)
    args = parser.parse_args()

    try:
        input_data = parse_input(args.input)
        main(input_data)
    except FileNotFoundError as e:
        print(e)
    except json.JSONDecodeError:
        print("Error: Failed to decode JSON from the input file.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
