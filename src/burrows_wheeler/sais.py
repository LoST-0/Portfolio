import numpy as np

###############################
#####       INIT        #######


def count_cumulative_characters(T, alphabet_size):
    B = np.zeros(alphabet_size, dtype=np.uint64)
    for i in T:
        B[i] += 1
    for i in range(1, alphabet_size):
        B[i] += B[i-1]
    return B


def compute_types(T):
    n = len(T)
    types = [None] * n
    types[n-1] = "S"
    for i in range(n-2, -1, -1):
        types[i] = "L" if T[i] > T[i+1] else "S" if T[i] < T[i+1] else types[i+1]
    return types


def find_lms_positions(types):
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


def initialize_pos_from_lms(T, B, lms, pos):
    pos[:] = -1  # Ignoto
    # Inseriamo le partizioni lms alla estrema destra del bucket
    for p in lms[::-1]:
        a = T[p]
        B[a] -= 1
        pos[B[a]] = p


def induce_L_positions(T, B, types, pos):
    n = len(T)
    for r in range(n):
        p = pos[r]
        if p <= 0:
            continue
        if types[p-1] == "S":
            continue
        a = T[p-1]
        pos[B[a-1]] = p-1
        B[a-1] += 1


def induce_S_positions(T, B, types, pos):
    n = len(T)
    for r in range(n-1, -1, -1):
        p = pos[r]
        if p <= 0:
            continue
        if types[p-1] == "L":
            continue
        a = T[p-1]
        B[a] -= 1
        pos[B[a]] = p-1


def phase2(T, B0, types, lms, pos):
    # Inizializziamo pos inserendo le LMS posizioni
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


def reduce_text(T, alph_size, types, pos, lms_positions):
    n, m = len(pos), len(lms_positions)
    names = np.full(n, -1, dtype=np.int64)
    last_lms = n-1
    names[last_lms] = 0  # Sentinella
    reduced_alph_size = 1
    j = 0
    # Per ogni suffisso in ordine lessicografico
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
    def isLMS(x): return (types[x] == "S" and types[x-1] == "L")
    while True:
        if T[p1] != T[p2]:
            return True
        if types[p1] != types[p2]:
            return True
        if is_lms_p1 and is_lms_p2:
            return False  # Equal
        p1 += 1
        p2 += 1
        is_lms_p1 = isLMS(p1)
        is_lms_p2 = isLMS(p2)
        if is_lms_p1 and is_lms_p2:
            continue
        if is_lms_p1 or is_lms_p2:
            return True


def phase1(T, B, types, lms_positions, pos):
    alph_size = len(B)
    phase2(T, B, types, lms_positions, pos)
    # Determiniamo i testi ridotti date le LMS sottostringhe
    R, reduced_alph_size, position_map = reduce_text(
        T, alph_size, types, pos, lms_positions)

    if len(R) != reduced_alph_size:
        reduced_pos = sais_construction_main(
            R, reduced_alph_size)  # Chiamata ricorsiva
        # Rimappiamo pos nelle posizioni originali
        for i, redp in enumerate(reduced_pos):
            lms_positions[i] = position_map[redp]
    return


def sais_construction_main(T, alphabet_size):
    pos = np.empty(len(T), dtype=np.int64)
    # Bucket limites
    B = count_cumulative_characters(T, alphabet_size)
    types = compute_types(T)  # S-L
    lms_positions = find_lms_positions(types)
    # PHASE 1
    phase1(T, B, types, lms_positions, pos)
    # PHASE 2
    phase2(T, B, types, lms_positions, pos)
    return pos

#Wrapper
def sais_construction(text):
  if text[-1] != "$":
        text += "$"
  converted, size = map_text_to_alphabet(text)
  suffix_array = sais_construction_main(converted, alphabet_size=size)
  return suffix_array
  

def map_text_to_alphabet(text):
    alph = list(set(text))
    alph.remove("$")
    alph.sort()
    alph.insert(0,"$")
    
    mapped = [alph.index(i) for i in text]
    return mapped, len(alph)


if __name__ == '__main__':
   print(sais_construction("abaaba$"))
