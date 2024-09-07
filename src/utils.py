import matplotlib.pyplot as plt
import random
import math


from functools import lru_cache


class TreeNode:
    def __init__(self, value, symbol=None):
        """Represents a node in a binary tree.

        Attributes:
            value: The value of the node.
            symbol: An optional symbol associated with the node.
            left: A reference to the left child node.
            right: A reference to the right child node.
        """
        self.value = value
        self.symbol = symbol
        self.left = None
        self.right = None

    def __lt__(self, other):
        """Defines the behavior of the < (less than) operator for TreeNode objects."""
        return self.value < other.value

    def __repr__(self):
        """Returns a string representation of the TreeNode."""
        return f"Node({self.value}, {self.symbol})"

@lru_cache(maxsize=64)
def fibonacci_word(order):
    """Generates a Fibonacci word of a given order.

    The Fibonacci word is constructed recursively:
    F(0) = "b", F(1) = "a", F(n) = F(n-1) + F(n-2).

    Args:
        order: The order of the Fibonacci word to generate.

    Returns:
        A string representing the Fibonacci word of the given order.
    """
    if order < 0:
        return ''
    elif order == 0:
        return "b"
    elif order == 1:
        return "a"
    else:
        return fibonacci_word(order - 1) + fibonacci_word(order - 2)


def count_equal_letter_run(text):
    """Counts the number of distinct runs of equal letters in a string.

    A run is defined as a maximal sequence of consecutive identical characters.

    Args:
        text: A string in which to count the runs.

    Returns:
        An integer representing the number of runs in the text.
    """
    if not text:
        return 0

    run_count = 1
    current_char = text[0]

    for char in text[1:]:
        if char != current_char:
            run_count += 1
            current_char = char

    return run_count

##### Integer Encoding #######

def get_custom_distribution(p, lower_bound=1, upper_bound=1000, step=1):
    """Generates a custom probability distribution based on a given probability function.

    Args:
        p: A function defining the probability distribution.
        lower_bound: The lower bound of the range of values.
        upper_bound: The upper bound of the range of values.
        step: The step size between consecutive values in the range.

    Returns:
        A list representing a distribution of values based on the custom probability function.
    """
    probabilities = []

    distribution = []
    for j in range(lower_bound, upper_bound + 1, step):
        probabilities.append(p(j))

    total_probability = sum(probabilities)
    normalized_probabilities = [prob / total_probability for prob in probabilities]

    for _ in range(lower_bound, upper_bound + 1, step):
        distribution.append(
            random.choices(
                population=range(lower_bound, upper_bound + 1, step),
                weights=normalized_probabilities,
                k=1
            )[0]
        )

    return distribution


def get_distribution(distribution_type=1, lower_bound=1, upper_bound=1000, step=1):
    """Generates a distribution based on a specified type.

    Args:
        distribution_type: The type of distribution to generate.
                          0: Uniform distribution
                          1: 1/(2x^2) distribution
                          2: 1/(2x(log(x))^2) distribution
        lower_bound: The lower bound of the range of values.
        upper_bound: The upper bound of the range of values.
        step: The step size between consecutive values in the range.

    Returns:
        A sorted list representing the generated distribution.
    """
    distribution = []
    p = lambda  x: x
    if distribution_type == 0:
        distribution.extend([
            random.randint(lower_bound, upper_bound)
            for _ in range(lower_bound, upper_bound + 1, step)
        ])
        distribution.sort()
        return distribution
    elif distribution_type == 1:
        p = lambda x: 1 / (2 * x ** 2)
    elif distribution_type == 2:
        p = lambda x: 1 / (2 * x * (math.log(x)) ** 2)

    distribution = get_custom_distribution(p, lower_bound=max(2, lower_bound), upper_bound=upper_bound, step=step)
    distribution.sort()
    return distribution


def plot_results(results: list[list[int]], test_range: list[int], compressors,
                 title="Compression Results of Different Compressors"):
    """Plots the results of different compression algorithms.

    Args:
        results: A list of lists, where each sublist contains the compression results for a given compressor.
        test_range: A list representing the range of the original data.
        compressors: A list of compressor functions/classes.
        title: A string representing the title of the plot.
    """
    num_compressors = len(results)
    plt.figure(figsize=(10, 6))
    for i in range(num_compressors):
        compressed_lengths = [len(result) for result in results[i]]
        plt.plot(test_range, compressed_lengths, label=f'{compressors[i].__name__}')

    plt.xlabel('Original Data')
    plt.ylabel('Length of Compressed Data')
    plt.title(title)
    plt.tight_layout()
    plt.legend()
    plt.show()

    return


###### String Attractors ######
def get_runs(bwt_text: str) -> list:
    """
    Identifies the start positions of each run in the Burrows-Wheeler Transform (BWT) text.

    Args:
        bwt_text: A string representing the BWT of the original text.

    Returns:
        A list of integers representing the start positions of each run in the BWT text.
    """
    runs = []
    current_run_char = bwt_text[0]
    run_start_position = 0

    for i in range(1, len(bwt_text)):
        if bwt_text[i] != current_run_char:
            runs.append(run_start_position)
            current_run_char = bwt_text[i]
            run_start_position = i


    runs.append(run_start_position)
    return runs


def __get_cyclic_rotations(text) -> list:
    """
    Generates all cyclic rotations of a given string.

    Args:
        text: A string to generate cyclic rotations for.

    Returns:
        A list of tuples, where each tuple contains a cyclic rotation and its original starting position.
    """
    return [(text[x:] + text[:x],x) for x in range(len(text))]


def get_string_attractor_from_bwt(text: str) -> list:
    """
    Generate the string attractor based on the BWT of the text.

    Parameters:
    bwt_text (str): The BWT of the text.
    text (str): The original text (assumed to include the special symbol $ at the end).

    Returns:
    list: The positions that form the string attractor.
    """

    rotations = __get_cyclic_rotations(text + "$")
    rotations = sorted(rotations, key=lambda x: x[0])

    bwt_text = ''.join([rotation[0][-1] for rotation in rotations])


    run_positions_in_bwt = get_runs(bwt_text)

    needed = [rotations[i][1] for i in run_positions_in_bwt]

    needed.remove(0)

    return sorted(needed)


def get_string_attractor_from_lz(lz_tokens:list) ->list:
    """
    Generates the string attractor based on LZSS compression tokens.

    Args:
        lz_tokens: A list of LZSS compression tokens.

    Returns:
        A list of integers representing the positions that form the string attractor.
    """
    pos = 0  # Current position in the original text
    attractor = []
    for token in lz_tokens:
        if isinstance(token, tuple) and token[0] == 0:
            attractor.append(pos)  #
            pos += 1  # Move to the next position in the text
        elif isinstance(token, tuple) and token[0] != 0:

            offset, length = token
            start_pos = pos
            attractor.append(start_pos)

            # Move position forward by the length of the match
            pos += length

    return sorted(attractor)


def generate_sturmian_word(alpha: float, rho: float, length: int) -> str:
    """
    Generates a finite Sturmian word based on the slope alpha and intercept rho.

    Args:
        alpha: The slope of the Sturmian word, an irrational number (0 < alpha < 1).
        rho: The intercept of the Sturmian word, a real number (0 <= rho < 1).
        length: The length of the Sturmian word to generate.

    Returns:
        A string representing the finite Sturmian word of the given length.
    """
    sturmian_word = ""

    # Generating the Sturmian word by checking the fractional part of (i * alpha + rho)
    for i in range(length):
        value = (i * alpha + rho) % 1
        if value < alpha:
            sturmian_word += '0'
        else:
            sturmian_word += '1'

    return sturmian_word


def balanced_parenthesis_word(n):
    """
    Generates all balanced parenthesis words of length 2n.

    :param n: The number of pairs of parentheses.
    :return: A list of strings, each representing a balanced parenthesis word.
    """

    def generate_parentheses(current_string, open_count, close_count, n, result):
        """Recursively generates balanced parenthesis words."""
        # If the current string length is 2n, add to result
        if len(current_string) == 2 * n:
            result.append(current_string)
            return

        # Add an opening parenthesis if open_count is less than n
        if open_count < n:
            generate_parentheses(current_string + '1', open_count + 1, close_count, n, result)

        # Add a closing parenthesis if close_count is less than open_count
        if close_count < open_count:
            generate_parentheses(current_string + '0', open_count, close_count + 1, n, result)

    result = []
    generate_parentheses('', 0, 0, n, result)
    return result

@lru_cache(maxsize=128)
def generate_binary_strings_recursive(n):
    """
    Generates all binary strings of length `n` using recursion.

    This function recursively generates all possible combinations of binary strings (composed of '0' and '1')
    of a given length `n`.

    Args:
        n: An integer representing the length of the binary strings to generate.

    Returns:
        A list of strings, where each string is a binary string of length `n`.

    Raises:
        None
    """
    # Base case: if n is 0, return an empty string

    if n == 0:
        return ['']

    # Recursive step: get binary strings of length n-1
    smaller_strings = generate_binary_strings_recursive(n - 1)

    # Initialize an empty list to store strings of length n
    result = []

    # Append '0' and '1' to each of the strings from the smaller_strings
    for s in smaller_strings:
        result.append(s + "0")
        result.append(s + "1")

    return result


######## SGP

def generate_random_text(alphabet, run_equal, len_text):
    """Generates a random text string with specified run lengths.

    This function generates a random text string of length `len_text` using the given `alphabet`.
    The text is composed of repeated characters (runs) with a maximum length of `run_equal`.

    Args:
        alphabet: A list of characters from which the text will be generated.
        run_equal: An integer representing the maximum length of runs of equal characters.
        len_text: An integer representing the total length of the generated text.

    Returns:
        A string representing the generated text.

    Raises:
        ValueError: If the alphabet is empty, or if `run_equal` or `len_text` is not a positive integer.
    """
    if not alphabet or run_equal <= 0 or len_text <= 0:
        raise ValueError(
            "Alphabet must not be empty, and run_equal and len_text must be positive integers.")

    text = []
    while len(text) < len_text:
        char = random.choice(alphabet)
        run_length = min(run_equal, len_text - len(text))
        text.extend(char * run_length)

    return ''.join(text)

##### LZ and BWT


def set_Tk(k, i):
    """Generates a list of specific binary patterns based on the given parameters.

       This function creates a list of binary patterns by appending 'b' repeated `(j ** k)` times to 'a',
       for all `j` from 1 to `i-1`.

       Args:
           k: An integer used as the exponent in the pattern generation.
           i: An integer representing the upper bound of the pattern generation loop.

       Returns:
           A list of strings, where each string follows the pattern 'a' + 'b' * (j ** k).

       Raises:
           None
    """
    i = max(1, i)
    Tk = []
    for j in range(1, i):
        Tk.append("a" + "b" * (j ** k))
    return Tk


def set_Wk(k=5):
    """Generates a list of specific binary patterns based on the given parameter `k`.

    This function creates a list of binary patterns, including specific sequences formed by
    concatenating 'a' and 'b' characters, and applying certain rules based on the input `k`.

    Args:
        k: An integer representing the pattern complexity. Defaults to 5.

    Returns:
        A list of strings, where each string follows specific patterns defined by the input `k`.

    Raises:
        None
    """
    k = max(k, 5)
    qk = "a" + "b" * k + "a"
    si = lambda x: "a" + "b" * x + "aa"
    ei = lambda x: "a" + "b" * x + "ab" + "a" * (x - 2)
    Wk = []
    for i in range(2, k):
        Wk.append(si(i) + ei(i))

    Wk.append(qk)
    return Wk

