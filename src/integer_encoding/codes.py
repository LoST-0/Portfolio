import math
from functools import lru_cache


class IntegerEncoder:
  """
    Abstract base class for integer coding algorithms.

    Attributes:
        __name__ (str): The name of the Encoder.
  """
  def __init__(self, name) -> None:
    """
      Initializes the IntegerEncoder with a name.

      Args:
          name (str): The name of the Encoder.
    """
    self.__name__ = name
    pass

  def encode(self, integers: list) -> list:
    """
      Encode a list of integers. This method should be overridden by subclasses.

      Args:
          integers (list): A list of integers to encode.

      Returns:
          list: A list of encoded data.
    """

    raise NotImplementedError

  def decode(self, encoded_integers: list) -> list:
    """
      Decodes a list of encoded integers. This method should be overridden by subclasses.

      Args:
          encoded_integers (list): A list of encoded data.

      Returns:
          list: A list of decoded integers.
    """
    raise NotImplementedError


class BinaryEncoder(IntegerEncoder):
  """
    Encoding algorithm that converts integers to binary representation.

    Attributes:
        bit_limit (int): The number of bits used to represent each integer.
  """
  def __init__(self):
    """
      Initializes the BinaryEncoder.
    """

    super().__init__("BinaryEncoder")
    self.bit_limit = None

  def encode(self, integers: list, optim=False) -> list:
    """
      Encodes integers by converting them to binary strings.

      Args:
          integers (list): A list of integers to encode.
          optim (bool): Whether to optimize the bit limit (default is False).

      Returns:
          list: A list of binary strings representing the encoded integers.
    """
    m = max(integers)
    self.bit_limit = 1 + math.ceil(math.log(m, 2)) if not optim else 0

    encoded = [bin(number)[2:].zfill(self.bit_limit) for number in integers]
    return encoded

  def decode(self, encoded_integers: list) -> list:
    """
      Decodes binary strings back to integers.

      Args:
          encoded_integers (list): A list of binary strings to decode.

      Returns:
          list: A list of decoded integers.
    """
    return [int(integer, 2) for integer in encoded_integers]


class UnaryEncoder(IntegerEncoder):
  """
    Encoding algorithm using unary encoding.
  """
  def __init__(self) -> None:
    """
      Initializes the UnaryEncoder.
    """
    super().__init__("UnaryEncoder")

  def encode(self, integers: list) -> list:
    """
      Encodes integers using unary encoding.

      Args:
          integers (list): A list of integers to encode.

      Returns:
          list: A list of unary-encoded strings.
    """
    return [''.zfill(integer - 1) + "1" for integer in integers]

  def decode(self, encoded_integers: list) -> list:
    """
      Decodes unary-encoded strings back to integers.

      Args:
          encoded_integers (list): A list of unary-encoded strings to decode.

      Returns:
          list: A list of decoded integers.
    """
    return [encoded.count('0') + 1 for encoded in encoded_integers]


class GammaEncoder(IntegerEncoder):
  """
    Encoding algorithm using gamma encoding.
  """

  def __init__(self) -> None:
    """
      Initializes the GammaEncoder.
    """
    super().__init__("GammaEncoder")

  def encode(self, integers: list) -> list:
    """
      Encodes integers using gamma encoding.

      Args:
          integers (list): A list of integers to encode.

      Returns:
          list: A list of gamma-encoded strings.
    """
    encoded = []
    for integer in integers:
      B = bin(integer)[2:]
      encoded.append(
          ''.zfill(len(B)-1) + B
      )
    return encoded

  def decode(self, encoded_integers: list[str]) -> list:
    """
      Decodes gamma-encoded strings back to integers.

      Args:
          encoded_integers (list): A list of gamma-encoded strings to decode.

      Returns:
          list: A list of decoded integers.
    """
    decoded = []
    for cinteger in encoded_integers:
      index = cinteger.index("1")
      decoded.append(
          int(cinteger[index:], 2)
      )

    return decoded


class DeltaEncoder(IntegerEncoder):
  """
    Encoding algorithm using delta encoding.
  """
  def __init__(self) -> None:
    """
      Initializes the DeltaEncoder with a GammaEncoder instance for gamma encoding.
    """
    super().__init__("DeltaEncoder")
    self.gEncoder = GammaEncoder()

  def encode(self, integers: list) -> list:
    """
      Encodes integers using delta encoding.

      Args:
          integers (list): A list of integers to encode.

      Returns:
          list: A list of delta-encoded strings.
    """
    bintegers = list(map(lambda x: bin(x)[2:], integers))
    g_len_bintegers = self.gEncoder.encode(
        list(map(len, bintegers))
    )
    encoded = [gbinlen + binteger[1:]
                  for binteger, gbinlen in zip(bintegers, g_len_bintegers)]
    return encoded

  def decode(self, encoded_integers: list[str]) -> list:
    """
      Decodes delta-encoded strings back to integers.

      Args:
          encoded_integers (list): A list of delta-encoded strings to decode.

      Returns:
          list: A list of decoded integers.
    """
    decoded = []
    for cinteger in encoded_integers:
      L = cinteger.index("1")
      N = "1" + cinteger[2*L+1:]
      decoded.append(
          int(N, 2)
      )
    return decoded


class FibonacciEncoder(IntegerEncoder):
  """
    Encoding algorithm using Fibonacci encoding.
  """
  def __init__(self) -> None:
    """
      Initializes the FibonacciEncoder.
    """
    super().__init__("FibonacciEncoder")

  @lru_cache(maxsize=128)
  def __fibonacci(self, n):
      """
        Computes the nth Fibonacci number using memoization.

         Args:
             n (int): The position in the Fibonacci sequence.

        Returns:
                int: The nth Fibonacci number.
     """
      if n == 0:
          return 0
      elif n == 1:
          return 1
      else:
          return self.__fibonacci(n - 1) + self.__fibonacci(n - 2)

  def nearest_fibonacci(self, num):
      """
      Finds the nearest Fibonacci number less than or equal to `num`.

      Args:
          num (int): The number to compare against Fibonacci numbers.

      Returns:
          tuple: The nearest Fibonacci number and its index in the sequence.
      """
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
      """
      Decomposes an integer into a sum of Fibonacci numbers.

      Args:
          integer (int): The integer to decompose.
          elements (list): A list to hold the Fibonacci numbers used in the sum.
          index (int): The current index in the decomposition process.

      Returns:
          list: A list of tuples where each tuple contains a Fibonacci number and its index.
      """
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
    """
      Encodes a sequence of Fibonacci numbers into a binary string.

      Args:
          sequence (list): A list of tuples where each tuple contains a Fibonacci number and its index.

      Returns:
          str: The encoded binary string.
    """
    _, max_index = sequence[0]
    fib = [0]*(max_index-2) + [1]
    for (_, v) in sequence:
      if v - 2 >= 0:
        fib[v-2] = 1
    fib.append(1)

    return ''.join(list(map(str, fib)))

  def __fibonacci_decode(self, finteger: str):
    """
      Decodes a Fibonacci-encoded binary string back to an integer.

      Args:
          finteger (str): The Fibonacci-encoded binary string.

      Returns:
          int: The decoded integer.
    """
    integer = 0
    for i, bit in enumerate(finteger):
      bit = int(bit, 2)
      integer += self.__fibonacci(i+2) if bit else 0

    return integer

  def encode(self, integers: list) -> list:
    """
      Encodes integers using Fibonacci encoding.

      Args:
          integers (list): A list of integers to encode.

      Returns:
          list: A list of Fibonacci-encoded strings.
    """
    encoded = []
    for integer in integers:
      fibonaccis_sequence = self.__get_fibonacci_sum(integer, [], 0)
      finteger = self.__fibonacci_encode(fibonaccis_sequence)
      encoded.append(finteger)
    return encoded

  def decode(self, encoded_integers: list) -> list:
     """
      Decodes Fibonacci-encoded strings back to integers.

      Args:
          encoded_integers (list): A list of Fibonacci-encoded strings to decode.

      Returns:
          list: A list of decoded integers.
     """
     decoded = []
     for finteger in encoded_integers:
       finteger = finteger[:-1]
       integer = self.__fibonacci_decode(finteger)
       decoded.append(integer)

     return decoded


class RiceEncoder(IntegerEncoder):
  """
    Encoding algorithm using Rice encoding.
  """

  def __init__(self, k=5) -> None:
    """
      Initializes the RiceEncoder with a parameter k.

      Args:
          k (int): The parameter for Rice encoding (default is 5).
    """
    super().__init__(f"RiceEncoder K{k}")
    self.k = 5
    self.powk = 2 << k
    self.uEncoder = UnaryEncoder()

  def encode(self, integers: list[int]) -> list[str]:
    """
      Encodes integers using Rice encoding.

      Args:
          integers (list[int]): A list of integers to encode.

      Returns:
          list[str]: A list of Rice-encoded strings.
    """
    encoded = []
    for integer in integers:
      q = (integer-1) // self.powk
      r = integer - (self.powk*q) - 1
      U = self.uEncoder.encode([q+1])[0]
      F = bin(r)[2:].zfill(self.k
      )
      encoded.append(U + F)

    return encoded

  def decode(self, encoded_integers: list[str]) -> list[int]:
    """
      Decodes Rice-encoded strings back to integers.

      Args:
          encoded_integers (list[str]): A list of Rice-encoded strings to decode.

      Returns:
          list[int]: A list of decoded integers.
    """
    decoded = []

    for rinteger in encoded_integers:

      end_unary = rinteger.index("1")

      U = rinteger[:end_unary+1]
      F = rinteger[end_unary+1:]
      q = self.uEncoder.decode([U])[0] - 1
      r = int(F, 2)

      x = self.powk * q + r + 1
      decoded.append(x)

    return decoded
