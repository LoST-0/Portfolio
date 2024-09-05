from src.string_attractors.gamma import StringAttractor
from src.lempel_ziv.lzSS import  LZSS
from src.burrows_wheeler.burrows_wheeler_transform import BWT
from src.utils import *



def testcase1(text):
    print("----- TEST 1 -----")
    checker = StringAttractor()
    bwt = BWT()
    lzss = LZSS(window_size=16)
    bwt_text,_ = bwt.transform(text)
    lz_text = lzss.compress(text)

    r = count_equal_letter_run(bwt_text)

    bwt_gamma = get_string_attractor_from_bwt(text,bwt_text)

    z = len(lz_text)
    lz_gamma = get_string_attractor_from_lz(lz_text)
    print(f"BWT({text})={bwt_text}")
    print(f"LZSS({text})={lz_text}")
    print(f"g_bwt(w): {bwt_gamma}, r :{r}")
    print(f"lz_gamma: {lz_gamma},  z:{z}")
    checker.positions = bwt_gamma
    bwtg = checker.is_string_attractor_for(text)
    checker.positions = lz_gamma
    lzg  = checker.is_string_attractor_for(text)

    assert bwtg
    assert lzg

    print("----- END 1 -----")
    return

def testcase2(n=20):
    print("----- TEST 2 -----")
    #alpha = (1 + 5 ** 0.5) / 2 - 1
    #rho = 0.0
    #sturmian_word = generate_sturmian_word(alpha,rho,n)
    fibo_word  = [fibonacci_word(i) for i in range(1,n)]
    bwt = BWT()

    for text in fibo_word:
        bwt_text,_ = bwt.transform(text)
        gamma = get_string_attractor_from_bwt(text,bwt_text)
        print(gamma,len(gamma))
        print(text)

    print("----- END 2 -----")
    return


def testcase3(n=8):
    print("----- TEST 3 -----")
    bstrings = generate_binary_strings_recursive(n)
    bwt = BWT()
    mapping = lambda x: len(get_string_attractor_from_bwt(x,bwt.transform(x)[0]))
    attractors_len = list(map(mapping, bstrings))
    minimal_len = [bstring for bstring,battractor in zip(bstrings,attractors_len)  if battractor == 2 ]

    for string in minimal_len:
        print(string)

    print("----- END 3 -----")
    return


def main():
    text = "ccbbccccaabbccccaaaa"
    testcase1(text)
    testcase2()
    testcase3()

    return



if __name__ == '__main__':
    main()