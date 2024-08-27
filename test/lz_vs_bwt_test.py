
from src.utils import *
from src.lempel_ziv.lz77 import LZ77
from src.burrows_wheeler.burrows_wheeler_transform import BWT






def main():

  rs = []
  zs = []
  bwt = BWT()
  lz77 = LZ77(window_size=16)

  k = 7
  strings = [
    fibonacci_word(k),
    fibonacci_word(k+1),
  ] + set_Tk(k,i=2) + set_Wk(k)

  for string in strings:
    bwt_transform,_ = bwt.transform(string)
    lz77_transform = lz77.compress(string)
    r = count_equal_letter_run(bwt_transform)
    z = len(lz77_transform)
    rs.append(r)
    zs.append(z)

  assert  len(strings) == len(rs) == len(zs)

  for i in range(len(strings)):

    print(f"String: {strings[i]}")
    print(f"r: {rs[i]}")
    print(f"z: {zs[i]}")
    log_n = math.log(len(strings[i]), 2)

    print(f"Empirical results:")
    print(f"{zs[i]} = O({rs[i]*log_n})")
    print(f"{rs[i]} = O({zs[i]*(log_n**2)})")
    print("------------------------------")


  return



if __name__ == '__main__':
  main()