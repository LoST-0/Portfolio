from collections import defaultdict

class StringAttractor:
    def __init__(self, positions=None):
        self.positions = positions or []
    @staticmethod
    def get_substring_occurrences(T):
      """
      Get a dictionary where keys are substrings of T and values are lists of starting positions of these substrings.
      """

      occurrences = defaultdict(list)
      n = len(T)

      for i in range(n):
        for j in range(i, n):
          substring = T[i:j + 1]
          occurrences[substring].append(i)

      return occurrences

    @staticmethod
    def intersects_with_attractor(substring_start, substring_end, G):
      """
      Check if the substring from substring_start to substring_end in T intersects with any position in G.
      """
      for pos in range(substring_start, substring_end + 1):
        if pos  in G:
          return True

      return False

    def is_string_attractor_for(self,T):
      """
      Verify if set G is a valid string attractor for string T.

      Parameters:
      T (str): The input string.
      G (set): The set of positions (1-based) to be checked as a string attractor.

      Returns:
      bool: True if G is a valid string attractor, False otherwise.
      """
      occurrences = self.get_substring_occurrences(T)

      for substring, starts in occurrences.items():
        valid = False

        for start in starts:
          end = start + len(substring) - 1

          if self.intersects_with_attractor(start, end, self.positions):
            valid = True
            break

        if not valid:
          return False

      return True

    @staticmethod
    def show_attractor(text,positions):
      print(text)
      print(''.join(
        "^" if i in positions else " "
        for i in range(len(text))
      ))

def main():
    positions = {2, 3, 4, 6}
    text = "1324321324"
    s = StringAttractor(positions=positions)
    s.show_attractor(text, positions)
    print(s.is_string_attractor_for(T=text))

    positions = {0, 1, 2, 3}
    text = "1324321324"
    s.positions = positions
    s.show_attractor(text, positions)
    print(s.is_string_attractor_for(T=text))


    positions = {2,4,6}
    text = "𝑎𝑏𝑏𝑎𝑎𝑏𝑎𝑏𝑏𝑎𝑎𝑏"
    s.positions = positions
    s.show_attractor(text, positions)
    print(s.is_string_attractor_for(T=text))

    positions = {4,6,9,10}
    text = "aaabaaaaaba"
    s.positions = positions
    s.show_attractor(text, positions)
    print(s.is_string_attractor_for(T=text))



if __name__ == "__main__":
    main()


# https://dspace.cvut.cz/bitstream/handle/10467/111201/F4-BP-2023-Hendrychova-Veronika-bp_mi_minf_23_hendrychova.pdf?sequence=-1&isAllowed=y





