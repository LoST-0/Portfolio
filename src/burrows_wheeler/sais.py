from typing import Any

import numpy as np


###############################
#####       INIT        #######


def count_cumulative_characters(text_converted:list, alphabet_size:int) -> np.ndarray:
    B = np.zeros(alphabet_size, dtype=np.uint32)
    for i in text_converted:
        B[i] += 1
    for i in range(1, alphabet_size):
        B[i] += B[i-1]
    return B


def compute_types(text_mapped) -> list:
    n = len(text_mapped)
    types = [None] * n
    types[n-1] = "S"
    for i in range(n-2, -1, -1):
        types[i] = "L" if text_mapped[i] > text_mapped[i + 1] else "S" if text_mapped[i] < text_mapped[i + 1] else types[i + 1]
    return types


def find_lms_positions(types:list[str]) -> np.ndarray:
    n = len(types)
    m = 0
    for p in range(1, n):
        m += (types[p] == "S" and types[p-1] == "L")

    lms_positions = np.empty(m, dtype=np.int64)
    m = 0
    for p in range(1, n):
        if types[p] == "S" and types[p-1] == "L":
            lms_positions[m] = p
            m += 1
    return lms_positions

###############################
#####      PHASE 2      #######

'''
Lemma:
    Within each bucket of the suffix array, L positions appear before the S-positions
    
Proof:
    Let p be an S-position and let q be an L-position, let s[p] = s[q] = b in alph. Both p and q are in the b-bucket.
    Then the suffix p+1, is larger than the suffix p, and suffix q+1 is smaller than suffix q.
    Because s[p] = s[q], the order of p and q is determined by p+1 and q+1, but q+1 cames before p+1 in the
    lexicographic order.
    
Example:
    Let a < b < c; suffix q is b+a, whereas p is b+c:
        q                      p
        bbbbbbbba       <      bbbbbbbbc
        L                      S   
        
Remainder:
    Given two LMS factors U and V (U != V) U <_{LMS} V if and only if:
    i) U[i] < V[i] for the smallest position i where U[i] != V[i] if exists
    ii) U[i] is L-type and V[i] is S-type or S*, for the smallest position i at which the two types differ
'''

'''
Correctness of phase 2:

Assuming correctly order LMS-positions in each bucket, then after step 2, all L-positions can be found at their correct positions

Proof:
    If p is a text position with rank r in pos and p-1 is a L-position, then p-1 has rank r' > r by definition of L-position.
    This assures that each L-position p-1 will:
        1) be induced by an LMS or L position p
        2) be induced by a position further to the left
        
Given all the type L-type (or S-type) suffixes of T, all the suffixes can be sorted in O(n) time

Proof:
    Let us suppose that all the L_type suffixes are correctly sorted, the proof is made by induction.
    For i = 1 is true by construction, hence SA[1]....S[j] are sorted.
    Let us suppose by contraddiction that T_{SA[i+1]} is not in the correct position. This means that exist in the same bucket
    T_{SA[k]} with k > i+1, such that T_{SA[k]} < T_{SA[i+1]} and both are L-type.
    T_{SA[k]} = cX and T_{SA[i+1]} = cY with X < Y. Since T_{SA[k]} is of L-type Y < T_{SA[K]} < T_{SA[i+1]}. Then Y must 
    occur in the first i position. Then T_{SA[k]} should appear before T_{SA[i+1]}!
    
Example:

    Consider the string "banana":
    
    1. The suffixes of "banana" are: "banana", "anana", "nana", "ana", "na", "a".
    
    2. Let's determine the L-type suffixes. L-type suffixes have a left smaller character, 
       so they are not sorted in lexicographical order:
    
       - "nana" and "na" are L-type because 'n' is greater than the following character 'a'.
       - "banana", "anana", "ana", and "a" are not L-type suffixes because they start with 
         smaller characters or are smaller suffixes.
    
    3. Suppose the L-type suffixes "nana" and "na" are correctly sorted in the suffix array (SA). 
       In this example, "na" comes before "nana" since it's shorter and lexicographically smaller.
    
    4. If we have T_{SA[i+1]} = "nana" and T_{SA[k]} = "na" with k > i+1, it means T_{SA[k]} 
       should appear before T_{SA[i+1]} in the suffix array because "na" (suffix starting with "na") 
       is lexicographically smaller than "nana" (suffix starting with "nana").
    
    Thus, by contradiction, our assumption was incorrect, and the L-type suffixes are correctly sorted.


'''


def initialize_pos_from_lms(text_mapped:list, buckets:list, lms:list, pos:list) -> None:
    """
    :param text_mapped: mapped text
    :param buckets: buckets list
    :param lms: lms positions indices
    :param pos: suffix array
    :return: None (pos would be modified)
    """
    pos[:] = -1  #Initialize pos with a sentinel at each position
    # Enter the sorted LMS suffix into pos at the rightmost-free position into ther bucket
    for p in lms[::-1]:
        a = text_mapped[p]
        buckets[a] -= 1 #set bucket pointers
        pos[buckets[a]] = p
    return


def induce_L_positions(text_mapped:list, buckets:list, types:list, pos:list) -> None:
    """
    :param text_mapped: mapped text
    :param buckets: buckets list
    :param types: position's types in mapped text
    :param pos:  suffix array
    :return:  None (pos would be modified)
    """
    # Left to Right scan of T
    for r in range(len(text_mapped)):
        # identify the position
        p = pos[r]
        if p <= 0: # is unknown ? then skip
            continue
        if types[p-1] == "S": # skip if S-type
            continue
        # p-1 is L-type
        a = text_mapped[p - 1] #get the character
        pos[buckets[a - 1]] = p - 1 #insert the position into the first position in the bucket
        buckets[a - 1] += 1 # update the pointer

    return


def induce_S_positions(text_mapped, buckets, types, pos) -> None:
    """
    :param text_mapped: mapped text
    :param buckets: buckets list
    :param types: position's types in mapped text
    :param pos:  suffix array
    :return:  None (pos would be modified)
    """
    n = len(text_mapped)
    # Right to Left scan of T
    for r in range(n-1, -1, -1):
        p = pos[r]
        if p <= 0: # is unknown ? then skip
            continue
        if types[p-1] == "L": # skip if L-type
            continue
         # p-1 is S-type
        a = text_mapped[p - 1] #get the character
        buckets[a] -= 1  #Point to the next right-most free position in its bucket
        pos[buckets[a]] = p - 1  # insert the position
    return


def phase2(T, B0, types, lms, pos):
    # Inizialize pos with the lms positions
    B = B0.copy()
    initialize_pos_from_lms(T, B, lms, pos)
    # Left to right scan  for L-pos
    B[:] = B0
    induce_L_positions(T, B, types, pos)
    # Right to left for S-pos
    B[:] = B0[:]
    induce_S_positions(T, B, types, pos)
    return




###############################
#####      PHASE 1      #######
"""
The goal for phase 1 is to sort the LMS suffixes, but is not very easy.
So instead we:

1) Sort the LMS substring up to the next LMS position, saving in time complexity: O(N)
2) Expand the alphabet and reduce the text (LMS substring -> character) keeping the lexicograph order of the LMS substrings
3) If all LMS substrings are distrincts we have reach our goal
4) Else we call recursively SAIS with the reduced text

The sorting phase could be done by simply use another run of phase 2:

1) Enter the unsorted LMS-position into the correct buckets of pos
2) Induce the order of L-positions based on the unsorted LMS-positions
3) induce the order of S-positions basef on the sorted L-positions

We will have the suffixes at LMS positions correctly sorted up to the next LMS position

"""


def reduce_text(T, types, pos, lms_positions):
    n, m = len(pos), len(lms_positions)
    names = np.full(n, -1, dtype=np.int64)
    last_lms = n-1
    names[last_lms] = 0  # Sentinel
    reduced_alph_size = 1
    j = 0
    # Per each suffix
    for r in range(1, n):
        p = pos[r]
        if p == 0 or types[p] != "S" or types[p-1] != "L":
            continue
        lms_positions[j] = p
        j += 1
        if lms_substrings_unequal(T, types, last_lms, p):
            reduced_alph_size += 1
        names[p] = reduced_alph_size - 1
        last_lms = p

    R = []
    position_map = {}
    for i, pos in enumerate(lms_positions):
        if pos != -1:
            R.append(names[pos])
            position_map[len(R) - 1] = pos

    return R, reduced_alph_size, position_map


def lms_substrings_unequal(T, types, p1, p2):
    # Ritorna vero se le sottostringhe LMS a p1 e p2 differiscono
    is_lms_p1 = is_lms_p2 = False
    def is_lms(x): return types[x] == "S" and types[x - 1] == "L"
    while True:
        if T[p1] != T[p2]:
            return True
        if types[p1] != types[p2]:
            return True
        if is_lms_p1 and is_lms_p2:
            return False  # Equal
        p1 += 1
        p2 += 1
        is_lms_p1 = is_lms(p1)
        is_lms_p2 = is_lms(p2)
        if is_lms_p1 and is_lms_p2:
            continue
        if is_lms_p1 or is_lms_p2:
            return True


def phase1(text_mapped, buckets, types, lms_positions, pos):

    phase2(text_mapped, buckets, types, lms_positions, pos)

    R, reduced_alph_size, position_map = reduce_text(
        text_mapped, types, pos, lms_positions)

    if len(R) != reduced_alph_size:
        reduced_pos = sais_construction_main(
            R, reduced_alph_size)

        for i, redp in enumerate(reduced_pos):
            lms_positions[i] = position_map[redp]
    return


def sais_construction_main(text_mapped, alphabet_size):
    pos = np.empty(len(text_mapped), dtype=np.int64)
    # Bucket limites
    B = count_cumulative_characters(text_mapped, alphabet_size)
    types = compute_types(text_mapped)  # S-L
    lms_positions = find_lms_positions(types)
    # PHASE 1
    phase1(text_mapped, B, types, lms_positions, pos)
    # PHASE 2
    phase2(text_mapped, B, types, lms_positions, pos)
    return pos

#Wrapper
def sais_construction(text:str) -> np.ndarray:
  if not text:
      raise ValueError("Empty text")

  if text[-1] != "$":
        text += "$"
  converted, size = map_text_to_alphabet(text)

  suffix_array = sais_construction_main(converted, alphabet_size=size)
  return suffix_array
  

def map_text_to_alphabet(text:str) -> tuple[list, int]:

    alph = list(set(text))
    alph.remove("$")
    alph.sort()
    alph.insert(0,"$")
    
    mapped = [alph.index(i) for i in text]
    return mapped, len(alph)


if __name__ == '__main__':
   print(sais_construction("banaananaanana$"))
