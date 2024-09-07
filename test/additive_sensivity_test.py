import matplotlib.pyplot as plt
from src.additive_sensitivity.additive_sensitivity import ADSMeasure


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
