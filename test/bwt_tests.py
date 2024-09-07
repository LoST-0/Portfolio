

import pandas as pd
from src.utils import *
from src.burrows_wheeler.burrows_wheeler_transform import BWT

def run_test(text, bwt):
    print("-" * 20)
    print("Running test sample: ", text)

    # Run BWT and inverse BWT
    L, I = bwt.transform(text)
    w = bwt.reverse_transform(L, I)

    print(f"BWT({text}): ", L)
    print(f"IBWT({L}): ", w)

    assert w == text, "Ops! The inverse BWT did not match the original text."

    r = count_equal_letter_run(L)

    print("SAIS-Test")
    # Construct the suffix array

    # Run BWT using SA-IS

    L, I = bwt.linear_transform(text)
    w = bwt.reverse_transform(L, I)

    print(f"SAIS-BWT({text}): ", L)
    print(f"SAIS-IBWT({L}): ", w)

    assert w == text + "$"
    rs = count_equal_letter_run(L)

    return r, rs


def main():
    order = 3
    bwt = BWT()
    testcases = [
        "amanaplanacanalpanama",
        fibonacci_word(order * 2),
        fibonacci_word(order * 3),
        fibonacci_word(order * 2)[:-1],
        fibonacci_word(order * 3)[:-1],
    ] + generate_binary_strings_recursive(5)

    runs = []
    for text in testcases:
        r, rs = run_test(text, bwt)
        runs.append((r, rs))

    # Create a pandas DataFrame for better visualization and manipulation
    df = pd.DataFrame(
         runs, columns=["Run BWT(T)", "Run BWT(T$)"])
    df.insert(0,'Word', testcases)

    print("-" * 20)
    print("Results:")
    print(df)

    df.plot(kind='bar', figsize=(10, 6))
    df.sort_values('Run BWT(T)', ascending=False, inplace=True)

    plt.title('BWT and SAIS-BWT Runs')
    plt.xlabel('Fibonacci Words')
    plt.ylabel('Number of Runs')
    plt.xticks(rotation=0)

    plt.show()

if __name__ == '__main__':
    main()