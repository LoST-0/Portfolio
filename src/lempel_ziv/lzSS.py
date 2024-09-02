from src.lempel_ziv.lz77 import  LZ


class LZSS(LZ):
  
  def __init__(self, window_size) -> None:
    super().__init__(window_size)
    self.text_len = None

  def __find_pair(self,text):
    
    sb_start = max(0, self.lk_begin - self.W)
    sb = text[sb_start:self.lk_begin]  
    lkb = text[self.lk_begin:]  

    if not lkb:
        return None  

    offset, match_len = self._find_max_prefix(sb,lkb)
    
    if offset == -1:
        return 0, lkb[0]
    real_offset = self.lk_begin - (sb_start + offset)
    
    return real_offset, match_len
  

  def compress(self, text: str) -> list:
      compressed_text = []
      self.lk_begin = 0
      self.text_len = len(text)

      while self.lk_begin < len(text):
            pair = self.__find_pair(text)
            if pair is None:
                break
            compressed_text.append(pair)

            self.lk_begin += 1 if isinstance(pair[1],str) else pair[1]

      return compressed_text
    
  @staticmethod
  def decompress(compressed_text: list) -> str:
     output = ""
     for v, p in compressed_text:
       if v:
         for _ in range(p):
           output += output[-v]
       else:
         output += p
         
     return output


def main():
  text = "aabbabab"
  compressor = LZSS(16)
  compressed_text = compressor.compress(text)
  decompresses_text = compressor.decompress(compressed_text)
  assert text == decompresses_text, "Ops, something went wrong!"
  print(compressed_text,decompresses_text)


if __name__ == "__main__":
  
  main()