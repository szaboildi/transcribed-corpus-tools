import ay_transcriber as ay_trans


##########################
# Counting one substring #
##########################
def count_subst(substr, st):
    """
    Count number of substrings in a set of words
    :param substr: substr to count
    :param st: set of words to count substr in
    :return: the number of occurrences of substr in st
    """
    subset = {item for item in st if substr in item}
    counter = 0

    for item in subset:
        counter += item.count(substr)

    return counter


############################
# Counting many substrings #
############################
def count_many_substr(substrings, words):
    """
    Count the number of multiple substrings in a set of words
    :param substrings: set of substrings to count
    :param words: set of words to count them in
    :return: dictionary of counts, where keys are the counted substrings,
    and values are their respective counts.
    """
    counts = {}
    for substr in substrings:
        count = count_subst(substr, words)
        counts[substr] = count

    return counts


def main():
    ay_words = ay_trans.set_reader("Outputs\\Transcription\\aymara_preprocessed.txt")
    plain_stops = ["p", "t", "c", "k", "q"]
    aspirates = ["P", "T", "C", "K", "Q"]
    ejectives = ["b", "d", "z", "g", "G"]
    stops = plain_stops + aspirates + ejectives
    fricatives = ["s", "S", "h", "x"]
    sonorants = ["m", "n", "N", "r", "l", "Y", "j", "w"]
    consonants = stops + fricatives + sonorants
    vowels = ["a", "A", "e", "E", "i", "I", "o", "O", "u", "U"]


if __name__ == "__main__":
    main()
