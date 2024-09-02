import math
from functools import lru_cache


class IntegerCompressor:
  def __init__(self, name) -> None:
    self.__name__ = name
    pass

  def compress(self, integers: list) -> list:
    raise NotImplementedError

  def decompress(self, compressed_integers: list) -> list:
    raise NotImplementedError


class BinaryCompressor(IntegerCompressor):

  def __init__(self):

    super().__init__("BinaryCompressor")
    self.bit_limit = None

  def compress(self, integers: list, optim=False) -> list:
    m = max(integers)
    self.bit_limit = 1 + math.ceil(math.log(m, 2)) if not optim else 0

    compressed = [bin(number)[2:].zfill(self.bit_limit) for number in integers]
    return compressed

  def decompress(self, compressed_integers: list) -> list:
    return [int(integer, 2) for integer in compressed_integers]


class UnaryCompressor(IntegerCompressor):

  def __init__(self) -> None:
    super().__init__("UnaryCompressor")

  def compress(self, integers: list) -> list:
    return [''.zfill(integer - 1) + "1" for integer in integers]

  def decompress(self, compressed_integers: list) -> list:
    return [compressed.count('0') + 1 for compressed in compressed_integers]


class GammaCompressor(IntegerCompressor):

  def __init__(self) -> None:
    super().__init__("GammaCompressor")

  def compress(self, integers: list) -> list:
    compressed = []
    for integer in integers:
      B = bin(integer)[2:]
      compressed.append(
          ''.zfill(len(B)-1) + B
      )
    return compressed

  def decompress(self, compressed_integers: list[str]) -> list:
    decompressed = []
    for cinteger in compressed_integers:
      index = cinteger.index("1")
      decompressed.append(
          int(cinteger[index:], 2)
      )

    return decompressed


class DeltaCompressor(IntegerCompressor):
  def __init__(self) -> None:
    super().__init__("DeltaCompressor")
    self.gcompressor = GammaCompressor()

  def compress(self, integers: list) -> list:
    bintegers = list(map(lambda x: bin(x)[2:], integers))
    g_len_bintegers = self.gcompressor.compress(
        list(map(len, bintegers))
    )
    compressed = [gbinlen + binteger[1:]
                  for binteger, gbinlen in zip(bintegers, g_len_bintegers)]
    return compressed

  def decompress(self, compressed_integers: list[str]) -> list:
    decompressed = []
    for cinteger in compressed_integers:
      L = cinteger.index("1")
      N = "1" + cinteger[2*L+1:]
      decompressed.append(
          int(N, 2)
      )
    return decompressed


class FibonacciCompressor(IntegerCompressor):

  def __init__(self) -> None:
    super().__init__("FibonacciCompressor")

  @lru_cache(maxsize=128)
  def __fibonacci(self, n):
      """Memoized function to compute the nth Fibonacci number."""
      if n == 0:
          return 0
      elif n == 1:
          return 1
      else:
          return self.__fibonacci(n - 1) + self.__fibonacci(n - 2)

  def nearest_fibonacci(self, num):
      """Function to find the nearest Fibonacci number less than or equal to `num`."""
      if num <= 0:
          return 0

      n = 0
      fib_n = self.__fibonacci(n)

      while fib_n <= num:
          n += 1
          next_fib_n = self.__fibonacci(n)
          if next_fib_n > num:
              break
          fib_n = next_fib_n

      return fib_n, n-1

  def __get_fibonacci_sum(self, integer, elements=None, index=0):

      if elements is None:
          elements = []

      if integer - index == 0:
          return elements

      # Get the largest Fibonacci number less than or equal to the remaining integer
      n, i = self.nearest_fibonacci(integer - index)

      elements.append((n, i))
      index += n

      return self.__get_fibonacci_sum(integer, elements, index)

  @staticmethod
  def __fibonacci_encode(sequence: list) -> str:

    _, max_index = sequence[0]
    fib = [0]*(max_index-2) + [1]
    for (_, v) in sequence:
      if v - 2 >= 0:
        fib[v-2] = 1
    fib.append(1)

    return ''.join(list(map(str, fib)))

  def __fibonacci_decode(self, finteger: str):
    integer = 0
    for i, bit in enumerate(finteger):
      bit = int(bit, 2)
      integer += self.__fibonacci(i+2) if bit else 0

    return integer

  def compress(self, integers: list) -> list:
    compressed = []
    for integer in integers:
      fibonaccis_sequence = self.__get_fibonacci_sum(integer, [], 0)
      finteger = self.__fibonacci_encode(fibonaccis_sequence)
      compressed.append(finteger)
    return compressed

  def decompress(self, compressed_integers: list) -> list:
     decompressed = []
     for finteger in compressed_integers:
       finteger = finteger[:-1]
       integer = self.__fibonacci_decode(finteger)
       decompressed.append(integer)

     return decompressed


class RiceCompressor(IntegerCompressor):

  def __init__(self, k=5) -> None:
    super().__init__("RiceCompressor")
    self.k = 5
    self.powk = pow(2, k)
    self.ucompressor = UnaryCompressor()

  def compress(self, integers: list[int]) -> list[str]:

    compressed = []
    for integer in integers:
      q = (integer-1) // self.powk
      r = integer - (self.powk*q) - 1
      U = self.ucompressor.compress([q+1])[0]
      F = bin(r)[2:].zfill(self.k
      )
      compressed.append(U + F)

    return compressed

  def decompress(self, compressed_integers: list[str]) -> list[int]:

    decompressed = []

    for rinteger in compressed_integers:

      end_unary = rinteger.index("1")

      U = rinteger[:end_unary+1]
      F = rinteger[end_unary+1:]
      q = self.ucompressor.decompress([U])[0] - 1
      r = int(F, 2)

      x = self.powk * q + r + 1
      decompressed.append(x)

    return decompressed
