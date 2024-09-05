class LZ:
    def __init__(self, window_size) -> None:
        self.W = window_size
        self.lk_begin = 0
        return

    @staticmethod
    def _find_max_prefix(sb: str, lkb: str):
        max_len = 0
        max_start = -1
        sb_len = len(sb)
        lkb_len = len(lkb)

        for i in range(sb_len - 1, -1, -1):
            j = 0
            while i + j < sb_len and j < lkb_len and sb[i + j] == lkb[j]:
                j += 1

            if j > max_len:
                max_len = j
                max_start = i

        return max_start, max_len


class LZ77Naive(LZ):
    def __init__(self, window_size) -> None:
        super().__init__(window_size)
        self.text_len = None

    @classmethod
    def _find_max_prefix(cls, sb: str, lkb: str):
        max_start, max_len = super(cls, cls)._find_max_prefix(sb=sb, lkb=lkb)
        if sb[max_start:max_start + max_len].startswith(lkb[max_len:-1]): #The last block repeats itself
            max_len += len(lkb[max_len:-1])
        return max_start, max_len

    def __find_triple(self, text: str):
    
        sb_start = max(0, self.lk_begin - (self.W // 2))
        sb = text[sb_start:self.lk_begin]  
        lkb = text[self.lk_begin:self.lk_begin + (self.W // 2)]

        if not lkb:
            return None  

        offset, match_len = self._find_max_prefix(sb, lkb)
                
        if offset == -1:
            return 0, 0, lkb[0]

        
        real_offset = self.lk_begin - (sb_start + offset)
        next_char = lkb[match_len] if match_len < len(lkb) else ''

        return real_offset, match_len, next_char

    def compress(self, text: str) -> list:
        compressed_text = []
        self.lk_begin = 0
        self.text_len = len(text)

        while self.lk_begin < len(text):
            triple = self.__find_triple(text)
            if triple is None:
                break  
            compressed_text.append(triple)

            self.lk_begin += triple[1] + 1

        return compressed_text

    @staticmethod
    def decompress(compressed_text:list) -> str:
        output = ""
        for triple in compressed_text:
            o,l,c = triple
            for _ in range(l):
                output += output[-o]
            output += c

        return output

def main():
  text = "aaaaaaaabbbbbbbb"
  compressor = LZ77Naive(16)
  compressed_text = compressor.compress(text)
  decompresses_text = compressor.decompress(compressed_text)
  assert text == decompresses_text, "Ops, something went wrong!"
  print(compressed_text,decompresses_text)

if __name__ == "__main__":
  main()
