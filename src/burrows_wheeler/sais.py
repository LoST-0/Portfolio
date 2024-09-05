

############################
#######   TESTING  #########
def build_suffix_array(text: str):
    suffixes = [(text[i:], i) for i in range(len(text))]
    suffixes.sort()
    suffix_array = [suffix[1] for suffix in suffixes]
    return suffix_array


def build_types_map(text):

    res = [-1] * (len(text) +1)
    res[-1] = "S"  # by definition

    if not len(text):
        return

    res[-2] = "L"

    n = len(text)
    for i in range(n-2,-1,-1):
        if text[i] > text[i+1]:
            res[i] = "L"
        elif text[i] == text[i+1] and res[i+1] == "L":
            res[i] = "L"
        else:
            res[i] = "S"
    return res

def is_lms_char(index,type_map):

    if index == 0: #The first position could not be an lms
        return  False

    return (type_map[index-1] == "L" and type_map[index] == "S")

def lms_substring_are_equal(text,type_map,pA,pB):

    if pA == len(text) or pB == len(text):
        return False

    i = 0
    while True:
        a_is_lms = is_lms_char(i + pA,type_map)
        b_is_lms = is_lms_char(i + pB,type_map)
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
        i+=1

##### Bucket Logic ######

def find_bucket_sizes(text_mapped,alph_size):

    res = [0] * alph_size
    for char in text_mapped:
        res[char] += 1

    return res


def find_bucket_heads(bucket_sizes):

    offset = 1
    res    = []
    for size in bucket_sizes:
        res.append(offset)
        offset += size

    return res

def find_bucket_tails(bucket_sizes):
    offset = 1
    res = []
    for size in bucket_sizes:
        offset += size
        res.append(offset - 1)

    return res
######################

##### RAW Logic ######

def raw_LMS_sort(string,bucket_sizes,type_map,debug=False):

      raw_suffix_array = [-1] * (len(string) +1)

      bucket_tails = find_bucket_tails(bucket_sizes)

      #Bucket-Sort all the LMS suffixes

      for i in range(len(string)):
          if not is_lms_char(i,type_map):
              # Not the start of an LMS suffix
            continue

          bucket_index = string[i] # What bucket ?
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


##### Iduced Sorting ######

def  induce_sort_L(string,raw_suffix_array,bucket_sizes,type_map,debug=False):

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
        bucket_heads[bucket_index] += 1 # Update the pointer
        if debug:
           show_suffix_array(raw_suffix_array,i)


def induce_sort_S(string, raw_suffix_array, bucket_sizes, type_map,debug=False):
    bucket_tails = find_bucket_tails(bucket_sizes)
    # For each cell in the suffix array
    for i in range(len(raw_suffix_array)-1,-1,-1):
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
'''
    Each LMS suffix of the original string gets a na,e. based on the order in wich those suffixes appear in the guessed suffix array
    Or rather, th eLMS substring at the beginning of each LMS suffix gets a name. IF two LMS suffix begin with the samecLMS substring, the get the same name
    These names are combined in the same order as the corresponding suffixes in the orignial string.

'''

def _summary_suffix_array( string,raw_suffix_array,type_map):

    lms_names = [-1] * (len(string) + 1 )

    current_name = 0

    last_lms_suffix_offset = None

    # The first LMS-substring will always be at position 0

    lms_names[raw_suffix_array[0]] = current_name
    last_lms_suffix_offset = raw_suffix_array[0]

    for i in range(1,len(raw_suffix_array)):
        # Where this suffix apper in the original string ?
        suffix_offset = raw_suffix_array[i]
        # Is LMS ?
        if not is_lms_char(suffix_offset,type_map):
            continue
        # If this LMS suffix start with a different LMS substring from the last we previusly looked
        if not lms_substring_are_equal(string,type_map,last_lms_suffix_offset,suffix_offset):
            # New name !
            current_name += 1


        last_lms_suffix_offset = suffix_offset
        # Store the name
        lms_names[suffix_offset] = current_name

    # Now lms_names contains all the characters og the suffix string in the correct order.
    # We now build a summary which tells us which LMS-suffix each item in the summary-string represents.

    summary_suffix_offsets = []
    summary_string = []

    for index,name in enumerate(lms_names):
        if name == -1:
            continue # Skip

        summary_suffix_offsets.append(index)
        summary_string.append(name)

    summary_alph_size = current_name + 1 #take in account 0


    return summary_string, summary_alph_size , summary_suffix_offsets

def make_summary_suffix_array(summary_string, summary_alph_size):

    if summary_alph_size == len(summary_string):
        # Every character of this summary string appears once and only once
        # so we can make the suffix array with a bucket sort
        summary_suffix_array_p = [-1] * (len(summary_string)+1)
        summary_suffix_array_p[0] = len(summary_string)
        for x in range(len(summary_string)):
            y = summary_string[x]
            summary_suffix_array_p[y+1] = x
    else:
        summary_suffix_array_p = make_suffix_array(summary_string,summary_alph_size ) #Recursion !
    return summary_suffix_array_p
#### SAIS

def show_suffix_array(array,pos=None):
    print("".join("%02d " %  each for each in array),)
    if pos is not None:
        print("".join(
            "^^  " if each == pos else "  " for each in range(len(array))
        ))
    return

def refined_LMS_sort(string,bucket_sizes,type_map,summary_suffix_array,summary_suffix_offsets):

    suffix_offsets = [-1] * (len(string) +1)
    #As before we'll be adding suffixes to the ends of their respective buckets
    #so to keep them in the right order ewr''l iterate througt summary_suffix_array in reverse

    bucket_tails = find_bucket_tails(bucket_sizes)

    for i in range(len(summary_suffix_array)-1,1,-1):

        string_index = summary_suffix_offsets[summary_suffix_array[i]]

        bucket_index = string[string_index]
        suffix_offsets[bucket_tails[bucket_index]] = string_index
        bucket_tails[bucket_index] -= 1


    suffix_offsets[0] = len(string)

    return  suffix_offsets




def make_suffix_array(string,alph_size,debug=False):

    #Classify each suffix
    type_map = build_types_map(string)
    # Compute the buckets
    bucket_sizes = find_bucket_sizes(string,alph_size)

    # Bucket-sort to insert all the LMS suffices into the approximately right place

    raw_suffix_array = raw_LMS_sort(string,bucket_sizes,type_map,debug=debug)

    #Slot all the other suffixes by using induced sorting.

    induce_sort_L(string,raw_suffix_array,bucket_sizes,type_map,debug=debug)

    induce_sort_S(string,raw_suffix_array,bucket_sizes,type_map,debug=debug)

    #Create a new string that summarises the relative order of lms suffices in the raw suffix array = Ranking

    summary_string,summary_alph_size,summary_suffix_offsets = _summary_suffix_array(string, raw_suffix_array,type_map )

    summary_suffix_array = make_summary_suffix_array(
        summary_string,
        summary_alph_size
    )


    result = refined_LMS_sort(string,bucket_sizes,type_map,summary_suffix_array,summary_suffix_offsets)


    induce_sort_L(string,result,bucket_sizes,type_map,debug=debug)
    induce_sort_S(string,result,bucket_sizes,type_map,debug=debug)


    return result


def map_text_to_alphabet(text: str) -> tuple[list, list]:
    alph = list(set(text))
    alph.sort()
    mapped = [alph.index(i) for i in text]
    return mapped,alph

def sais_construction(text:str):
    text,alph = map_text_to_alphabet(text)
    return make_suffix_array(text,len(alph))

def main():

    text = "baabaabac"
    first = build_suffix_array(text+"$")
    text,alph = map_text_to_alphabet(text)
    second = make_suffix_array(text,len(alph),debug=False)
    assert  first == second , "Ops!"



if __name__ == "__main__":
    main()

