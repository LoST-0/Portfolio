import matplotlib.pyplot as plt
from src.additive_sensitivity.additive_sensitivity import ADSMeasure

'''
    We remark that most instances of S^n are not compressible, or in other words, a randomly chosen string T from n is
    not compressible. Such a string T does not become highly compressible just after a one-character edit operation, and hence
    C(T) and C(T′) are expected to be almost the same. Therefore, considering the average sensitivity of string compressors and
    repetitiveness measures does not seem worth discussing, and this is the reason why we focus on the worst-case sensitivity
    of string compressors and repetitiveness measure

    "Sensitivity of string compressors and repetitiveness measures"
    Tooru Akagia , Mitsuru Funakoshia, Shunsuke Inenaga,
'''


def plot_sensitivity(results: list[int], title: str = "Additive Sensitivity"):
    plt.figure(figsize=(10, 6))
    plt.plot(range(1, len(results) + 1), results, marker='o', linestyle='-', color='b')
    plt.title(title)
    plt.xlabel("Order")
    plt.ylabel("Sensitivity")
    plt.grid(True)
    plt.show()


def test_additive_sensitivity():
    n = 15
    results: list[int] = []
    ads = ADSMeasure()

    for i in range(1, n+1):
        results.append(ads.additive_sensitivity(order=i))
    plot_sensitivity(results)


if __name__ == '__main__':
    test_additive_sensitivity()
