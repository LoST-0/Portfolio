from nis import match

from src.lempel_ziv.lz77naive import LZ77Naive,LZ

class LZ77(LZ77Naive):

    def __init__(self, window_size):
        super().__init__(window_size)

    @classmethod
    def _find_max_prefix(cls, sb: str, lkb: str):
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



