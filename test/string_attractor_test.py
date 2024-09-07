
from src.utils import *
from src.lempel_ziv.lzSS import  LZSS
from src.string_attractors.gamma import StringAttractor
from src.burrows_wheeler.burrows_wheeler_transform import BWT


def testcase1(text):
    print("----- TEST 1 -----")

    checker = StringAttractor()
    bwt = BWT()
    lzss = LZSS(window_size=16)

    bwt_text,_ = bwt.linear_transform(text)
    lz_text = lzss.compress(text)

    bwt_gamma = get_string_attractor_from_bwt(text)
    lz_gamma = get_string_attractor_from_lz(lz_text)

    z = len(lz_text)
    r = count_equal_letter_run(bwt_text)

    print(f"BWT({text})={bwt_text}")
    print(f"LZSS({text})={lz_text}")
    print(f"g_bwt(w): {bwt_gamma}, r :{r}")
    print(f"lz_gamma: {lz_gamma}, z :{z}")
    bwt_gamma = [x-1 for x in bwt_gamma]
    checker.positions = bwt_gamma
    bwtg = checker.is_string_attractor_for(text)

    checker.positions = lz_gamma
    lzg  = checker.is_string_attractor_for(text)

    print(bwtg,lzg)
    print("----- END 1 -----")
    return

def testcase2(n=10):
    print("----- TEST 2 -----")

    fibo_word  = [fibonacci_word(i) for i in range(1,n)]
    checker = StringAttractor()

    for text in fibo_word:
        gamma = get_string_attractor_from_bwt(text)
        gamma = [x-1 for x in gamma ]

        checker.positions = gamma
        print(f"[*] String:{text}\n"
              f"[*] Size:{len(gamma)}\n"
              f"[*] Attractor:{gamma}\n"
              f"[*] Check: {checker.is_string_attractor_for(text)}")
        checker.show_attractor(text, checker.positions)
    print("----- END 2 -----")
    return


def testcase3(n=8):
    print("----- TEST 3 -----")
    checker = StringAttractor()
    bstrings = generate_binary_strings_recursive(n)
    attractors = [get_string_attractor_from_bwt(x) for x in bstrings]
    attractors_len = [len(x) for x in attractors]
    minimal_len = [bstring  if battractor <= 3 else None for bstring,battractor in zip(bstrings,attractors_len) ]

    for index, string in enumerate(minimal_len):
        if string:
            checker.positions = [x-1 for x in attractors[index]]
            print(f"[*] Index:{index}\n[*] String:{string}\n"
                  f"[*] Size:{attractors_len[index]}\n"
                  f"[*] Attractor:{attractors[index]}\n"
                  f"[*] Check: {checker.is_string_attractor_for(string )}")

            checker.show_attractor(string,checker.positions)


            print()
    print("----- END 3 -----")
    return


def main():
    text = generate_sturmian_word(alpha=0.7,rho=0.2,length=10)
    testcase1(text)

    text = balanced_parenthesis_word(10)[15]

    testcase1(text)

    testcase2()

    testcase3()

    return



if __name__ == '__main__':
    main()