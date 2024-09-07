
from src.utils import fibonacci_word
############################
#######   TESTING  #########
"""
A naive implementation to build a suffix array for a given text.

The function generates all suffixes of the input string, sorts them lexicographically,
and then constructs a suffix array which is a list of starting positions of
these sorted suffixes.

:param text: The input string for which to build the suffix array.
:return: A list representing the suffix array of the input text.
"""
def build_suffix_array(text: str):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    suffix_array = [suffix[1] for suffix in suffixes]
    return suffix_array


#################

def build_types_map(text):
    """
    Assigns a type (S-type or L-type) to each character in the text based on the
    lexicographical order of the suffix that starts at that character.

    S-type (small type) suffix: Suffix T[i:] is S-type if T[i:] < T[i+1:].
    L-type (large type) suffix: Suffix T[i:] is L-type if T[i:] > T[i+1:].

    :param text: The input string for which to build the type map.
    :return: A list of types ('S' or 'L') corresponding to each character in the text.
    """
    res = [-1] * (len(text) +1)
    res[-1] = "S"  # by definition

    if not len(text):
        return

    res[-2] = "L"

    n = len(text)
    for i in range(n - 2, -1, -1):
        if text[i] > text[i + 1]:
            res[i] = "L"
        elif text[i] == text[i + 1] and res[i + 1] == "L":
            res[i] = "L"
        else:
            res[i] = "S"
    return res


def is_lms_char(index, type_map):
    """
    Determines whether the character at the given index is an LMS (Leftmost S-type) character.

    A character is considered an LMS character if it is S-type and the character preceding it is L-type.

    :param index: The index of the character in the text.
    :param type_map: The list of types ('S' or 'L') for each character in the text.
    :return: True if the character at the given index is an LMS character, False otherwise.
    """
    if index == 0:  #The first position could not be an lms
        return False

    return type_map[index - 1] == "L" and type_map[index] == "S"


def lms_substring_are_equal(text, type_map, pA, pB):
    """
    Checks if two LMS substrings starting at indices pA and pB in the text are equal.

    Two LMS substrings are considered equal if they match up to the next LMS character or differ
    earlier.

    :param text: The original string.
    :param type_map: The list of types ('S' or 'L') for each character in the text.
    :param pA: Starting index of the first LMS substring.
    :param pB: Starting index of the second LMS substring.
    :return: True if the LMS substrings are equal, False otherwise.
    """

    if pA == len(text) or pB == len(text):
        return False

    i = 0
    while True:
        a_is_lms = is_lms_char(i + pA, type_map)
        b_is_lms = is_lms_char(i + pB, type_map)
        # If we have found the beginning of the next LMS-string
        if i > 0 and (a_is_lms and b_is_lms):
            # And the string matches they are equal
            return True
        elif a_is_lms != b_is_lms:
            # We found an end before the other
            return False
        elif text[i + pA] != text[i + pB]:
            #A character difference !
            return False
        i += 1


##### Bucket Logic ######

def find_bucket_sizes(text_mapped, alph_size):
    """
    Creates an array that contains the number of suffixes that begin with each character in the alphabet.

    :param text_mapped: The text mapped to its corresponding alphabet indices.
    :param alph_size: The size of the alphabet.
    :return: A list where each element represents the number of suffixes starting with that character.
    """
    res = [0] * alph_size
    for char in text_mapped:
        res[char] += 1

    return res


def find_bucket_heads(bucket_sizes):
    """
    Creates an array where each element points to the head of a bucket, representing where the suffixes
    starting with a specific character should begin.

    :param bucket_sizes: A list containing the sizes of each bucket.
    :return: A list where each element points to the head of the corresponding bucket.
    """
    offset = 1
    res = []
    for size in bucket_sizes:
        res.append(offset)
        offset += size

    return res


def find_bucket_tails(bucket_sizes):
    """
    Creates an array where each element points to the tail of a bucket, representing where the suffixes
    starting with a specific character should end.

    :param bucket_sizes: A list containing the sizes of each bucket.
    :return: A list where each element points to the tail of the corresponding bucket.
    """
    offset = 1
    res = []
    for size in bucket_sizes:
        offset += size
        res.append(offset - 1)

    return res


##### RAW Logic ######

def raw_LMS_sort(string, bucket_sizes, type_map, debug=False):
    """
    Performs a bucket sort to place all LMS suffixes in their approximate positions in the suffix array.

    :param string: The text mapped to its corresponding alphabet indices.
    :param bucket_sizes: A list containing the sizes of each bucket.
    :param type_map: The list of types ('S' or 'L') for each character in the text.
    :param debug: If True, the function will print the suffix array at each step.
    :return: A list representing the raw suffix array after sorting LMS suffixes.
    """

    raw_suffix_array = [-1] * (len(string) + 1)
    bucket_tails = find_bucket_tails(bucket_sizes)

    #Bucket-Sort all the LMS suffixes

    for i in range(len(string)):
        if not is_lms_char(i, type_map):
            # Not the start of an LMS suffix
            continue

        bucket_index = string[i]  # What bucket ?
        # Add the start position at the tail of the bucket
        raw_suffix_array[bucket_tails[bucket_index]] = i
        # and move the pointer
        bucket_tails[bucket_index] -= 1
        if debug:
            show_suffix_array(raw_suffix_array)

    raw_suffix_array[0] = len(string)

    if debug:
        print("------")
        show_suffix_array(raw_suffix_array)
    return raw_suffix_array


##### Induced Sorting ######

def induce_sort_L(string, raw_suffix_array, bucket_sizes, type_map, debug=False):
    """
    Performs induced sorting to place L-type suffixes into their correct positions in the suffix array.

    :param string: The text mapped to its corresponding alphabet indices.
    :param raw_suffix_array: The partially sorted suffix array.
    :param bucket_sizes: A list containing the sizes of each bucket.
    :param type_map: The list of types ('S' or 'L') for each character in the text.
    :param debug: If True, the function will print the suffix array at each step.
    """

    bucket_heads = find_bucket_heads(bucket_sizes)

    # For each cell in the suffix array
    for i in range(len(raw_suffix_array)):

        if raw_suffix_array[i] == -1:
            continue

        j = raw_suffix_array[i] - 1
        if j < 0:
            # This entry in the suffix array is the suffix that begins at the start pf the string, offset 0.
            # Therefore, there is no suffix to its left.
            continue

        if type_map[j] != "L":
            # Only interested into L-type suffixes
            continue

        # Identify the bucket
        bucket_index = string[j]
        #add the start position to the HEAD of the bucket
        raw_suffix_array[bucket_heads[bucket_index]] = j
        bucket_heads[bucket_index] += 1  # Update the pointer
        if debug:
            show_suffix_array(raw_suffix_array, i)


def induce_sort_S(string, raw_suffix_array, bucket_sizes, type_map, debug=False):
    """
    Performs induced sorting to place S-type suffixes into their correct positions in the suffix array.

    :param string: The text mapped to its corresponding alphabet indices.
    :param raw_suffix_array: The partially sorted suffix array.
    :param bucket_sizes: A list containing the sizes of each bucket.
    :param type_map: The list of types ('S' or 'L') for each character in the text.
    :param debug: If True, the function will print the suffix array at each step.
    """
    bucket_tails = find_bucket_tails(bucket_sizes)
    # For each cell in the suffix array
    for i in range(len(raw_suffix_array) - 1, -1, -1):
        j = raw_suffix_array[i] - 1
        if j < 0:
            # This entry in the suffix array is the suffix that begins at the start pf the string, offset 0.
            # Therefore, there is no suffix to its left.
            continue

        if type_map[j] != "S":
            # Only interested into L-type suffixes
            continue

        # Identify the bucket
        bucket_index = string[j]
        # add the start position to the TAIL of the bucket
        raw_suffix_array[bucket_tails[bucket_index]] = j
        bucket_tails[bucket_index] -= 1  # Update the pointer
        #
        if debug:
            show_suffix_array(raw_suffix_array, i)
    #show_suffix_array(raw_suffix_array)


##### Summary logic  #####

def _summary_suffix_array(string, raw_suffix_array, type_map):
    """
    Creates a summary of the suffix array by assigning a unique name to each LMS (Leftmost S-type) substring
    in the original string. These names are then used to construct a summary string, which represents the
    order and relative positions of these LMS substrings in the original string.

    The function processes the suffix array and checks for LMS substrings, assigns names based on
    lexicographical order, and then constructs a summary string and a list of offsets where each
    LMS substring starts in the original string.

    :param string: The original string mapped to its corresponding alphabet indices.
    :param raw_suffix_array: The suffix array obtained after performing the initial sorting steps.
    :param type_map: The list of types ('S' or 'L') for each character in the text.
    :return: A tuple containing:
        - summary_string: A list representing the named LMS substrings in the correct order.
        - summary_alph_size: The size of the summary alphabet, indicating the number of unique LMS substrings.
        - summary_suffix_offsets: A list of starting positions for each LMS substring in the original string.
    """
    lms_names = [-1] * (len(string) + 1)

    current_name = 0
    last_lms_suffix_offset = None

    # The first LMS-substring will always be at position 0

    lms_names[raw_suffix_array[0]] = current_name
    last_lms_suffix_offset = raw_suffix_array[0]

    for i in range(1, len(raw_suffix_array)):
        # Where this suffix apper in the original string ?
        suffix_offset = raw_suffix_array[i]
        # Is LMS ?
        if not is_lms_char(suffix_offset, type_map):
            continue
        # If this LMS suffix start with a different LMS substring from the last we previusly looked
        if not lms_substring_are_equal(string, type_map, last_lms_suffix_offset, suffix_offset):
            # New name !
            current_name += 1

        last_lms_suffix_offset = suffix_offset
        # Store the name
        lms_names[suffix_offset] = current_name

    # Now lms_names contains all the characters og the suffix string in the correct order.
    # We now build a summary which tells us which LMS-suffix each item in the summary-string represents.
    summary_suffix_offsets = []
    summary_string = []

    for index, name in enumerate(lms_names):
        if name == -1:
            continue  # Skip

        summary_suffix_offsets.append(index)
        summary_string.append(name)

    summary_alph_size = current_name + 1  #take in account 0

    return summary_string, summary_alph_size, summary_suffix_offsets


def make_summary_suffix_array(summary_string, summary_alph_size):
    """
    Generates the suffix array for the summary string, which is a compressed representation of
    the original string containing only the LMS substrings.

    If the summary alphabet size is equal to the length of the summary string, it implies that
    each character in the summary string is unique, allowing the suffix array to be constructed
    directly using a bucket sort. Otherwise, the function recursively computes the suffix array
    using the same algorithm.

    :param summary_string: The list of names representing the LMS substrings in the original string.
    :param summary_alph_size: The number of unique LMS substrings, i.e., the size of the summary alphabet.
    :return: The suffix array of the summary string.
    """
    if summary_alph_size == len(summary_string):
        # Every character of this summary string appears once and only once
        # so we can make the suffix array with a bucket sort
        summary_suffix_array_p = [-1] * (len(summary_string) + 1)
        summary_suffix_array_p[0] = len(summary_string)
        for x in range(len(summary_string)):
            y = summary_string[x]
            summary_suffix_array_p[y + 1] = x
    else:
        summary_suffix_array_p = make_suffix_array(summary_string, summary_alph_size)  #Recursion !
    return summary_suffix_array_p


#### SAIS

def show_suffix_array(array, pos=None):
    print("".join("%02d " % each for each in array), )
    if pos is not None:
        print("".join(
            "^^  " if each == pos else "  " for each in range(len(array))
        ))
    return


def refined_LMS_sort(string, bucket_sizes, type_map, summary_suffix_array, summary_suffix_offsets):
    """
    Refines the LMS-sort by placing suffixes in the correct order based on the summary suffix array.

    :param string: The original string represented as a list of integers.
    :param bucket_sizes: The sizes of the buckets used for sorting.
    :param type_map: A map indicating the type (S-type or L-type) of each suffix in the original string.
    :param summary_suffix_array: The suffix array of the summary string.
    :param summary_suffix_offsets: The starting positions of the LMS substrings in the original string.
    :return: A refined suffix array for the original string.
    """
    suffix_offsets = [-1] * (len(string) + 1)
    #As before we'll be adding suffixes to the ends of their respective buckets
    #so to keep them in the right order ewr''l iterate througt summary_suffix_array in reverse

    bucket_tails = find_bucket_tails(bucket_sizes)

    for i in range(len(summary_suffix_array) - 1, 1, -1):
        string_index = summary_suffix_offsets[summary_suffix_array[i]]

        bucket_index = string[string_index]
        suffix_offsets[bucket_tails[bucket_index]] = string_index
        bucket_tails[bucket_index] -= 1

    suffix_offsets[0] = len(string)

    return suffix_offsets


def make_suffix_array(string, alph_size, debug=False):
    """
    Constructs the suffix array for a given string using the induced sorting algorithm (SA-IS).

    :param string: The original string represented as a list of integers.
    :param alph_size: The size of the alphabet used in the string.
    :param debug: A boolean flag to enable debugging output.
    :return: The suffix array of the original string.
    """

    #Classify each suffix
    type_map = build_types_map(string)
    # Compute the buckets
    bucket_sizes = find_bucket_sizes(string, alph_size)

    # Bucket-sort to insert all the LMS suffices into the approximately right place

    raw_suffix_array = raw_LMS_sort(string, bucket_sizes, type_map, debug=debug)

    #Slot all the other suffixes by using induced sorting.

    induce_sort_L(string, raw_suffix_array, bucket_sizes, type_map, debug=debug)

    induce_sort_S(string, raw_suffix_array, bucket_sizes, type_map, debug=debug)

    #Create a new string that summarises the relative order of lms suffices in the raw suffix array = Ranking

    summary_string, summary_alph_size, summary_suffix_offsets = _summary_suffix_array(string, raw_suffix_array,
                                                                                      type_map)

    summary_suffix_array = make_summary_suffix_array(
        summary_string,
        summary_alph_size
    )

    result = refined_LMS_sort(string, bucket_sizes, type_map, summary_suffix_array, summary_suffix_offsets)

    induce_sort_L(string, result, bucket_sizes, type_map, debug=debug)
    induce_sort_S(string, result, bucket_sizes, type_map, debug=debug)

    return result


def map_text_to_alphabet(text: str) -> tuple[list, list]:
    """
    Maps the characters of a string to their corresponding indices in the sorted alphabet.

    :param text: The original text string.
    :return: A tuple containing the mapped text as a list of integers and the sorted alphabet.
    """
    alph = list(set(text))
    alph.sort()
    mapped = [alph.index(i) for i in text]
    return mapped, alph


def sais_construction(text: str):
    """
    Constructs the suffix array for a given string using the SA-IS algorithm.

    :param text: The original text string.
    :return: The suffix array of the original string.
    """
    text, alph = map_text_to_alphabet(text)
    return make_suffix_array(text, len(alph))


def main():
    text = fibonacci_word(order= 8)
    first = build_suffix_array(text + "$") # Naive
    text, alph = map_text_to_alphabet(text)
    second = make_suffix_array(text, len(alph), debug=False)
    assert first == second, "Ops!"


if __name__ == "__main__":
    main()





### Credits to zork.net