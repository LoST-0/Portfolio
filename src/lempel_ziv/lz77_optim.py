from nis import match

from src.lempel_ziv.lz77naive import LZ77Naive,LZ

class LZ77(LZ77Naive):
    """
    Extended implementation of the LZ77 compression algorithm with improved
    handling of repetitive patterns in the look-ahead buffer.
    """

    def __init__(self, window_size):
        """
        Initializes the LZ77 class with a specified window size.

        Args:
            window_size (int): The size of the sliding window used in the compression.
        """
        super().__init__(window_size)

    @classmethod
    def _find_max_prefix(cls, sb: str, lkb: str):
        """
        Finds the longest prefix of `lkb` that matches a suffix of `sb`, with enhanced
        handling for repeated patterns in the look-ahead buffer.

        Args:
            sb (str): The string to search within (search buffer).
            lkb (str): The string to search for (look-ahead buffer).

        Returns:
            tuple: A tuple containing the start index and the length of the longest match.
        """
        max_start, max_len = LZ._find_max_prefix(sb, lkb)
        if max_start + max_len == len(sb):
            # At the beginning of the look-ahead buffer we check for repetitions
            sb_match = sb[max_start:max_start+max_len]
            i = 1
            # check for complete repetitions
            for repetition in range(2,len(lkb) // max_len):
                if lkb.startswith(sb_match * repetition):
                    i = repetition
            # check for partial repetitions
            sb_match = sb_match * i
            aux = 0
            for k,j in enumerate(lkb[len(sb_match):len(sb_match)+max_len]):
                if sb[max_start:max_start+k] == j:
                    aux += 1
                else:
                    break
            sb_match = sb_match + sb_match[:aux]
            max_len = len(sb_match)
        return max_start, max_len


def main():
  text = ("abracadabrarrarrararrarrarrarrarrar")
  compressor = LZ77(32)
  compressed_text = compressor.compress(text)
  decompresses_text = compressor.decompress(compressed_text)
  assert text == decompresses_text, "Ops, something went wrong!"
  print(compressed_text,decompresses_text)

if __name__ == "__main__":
  main()



