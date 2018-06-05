#!/usr/bin/python
import ay_transcriber as ay_trans
import re
import os


#######################
# Counting substrings #
#######################
## Counting one substring
def count_substr(substr, words):
    """
    Count the number of occurences of a substring in a set of words
    :param substr: substr to count
    :param words: set of words to count substr in
    :return: the number of occurrences of substr in st
    """
    subset = {item for item in words if substr in item}
    counter = 0

    for item in subset:
        counter += item.count(substr)

    return counter


## Counting one substring word-initially
def count_initial_substr(substr, words):
    """
    Count the number of occurences of a substring in a set of words,
    where the substring is word-initial
    :param substr: substr to count
    :param words: set of words to count substr in
    :return: the number of occurrences of substr in st
    """
    subset = {item for item in words if item.startswith(substr)}
    return len(subset)


## Counting many substrings (initial or any)
def count_many_substr(substrings, words, initial=False):
    """
    Count the number of occurences of multiple substrings in a set of words
    Can count only initial occurences or not
    :param substrings: set of substrings to count
    :param words: set of words to count them in
    :param initial: if the substring has to be initial, default False
    :return: dictionary of counts, where keys are the counted substrings,
    and values are their respective counts.
    """
    counts = {}
    for substr in substrings:
        if initial:
            count = count_initial_substr(substr, words)
        else:
            count = count_substr(substr, words)

        counts[substr] = count

    return counts

## Regular expressions:
def count_regexp(regexp, words):
    """
    Count words matching a regular expression pattern in a set of words
    :param regexp: Regular expression to be matched
    :param words: Set of words to search in
    :return: Number of matching words
    """
    subset = set(filter(lambda s: re.match(regexp, s), words))
    return len(subset)


####################
# Write dictionary #
####################
def write_dict(dict, path):
    """
    Writes dictionary into text file
    :param dict: dictionary to be written out
    :param path: path of file to be written to
    :return: None
    """
    with open(path, 'w', encoding='utf-8') as output_w:
        for key in dict.keys():
            output_w.write('{}\t{}\n'.format(key, int(dict[key])))



def main():
    ay_words = ay_trans.set_reader(os.path.join(*["Outputs",
                                                  "Transcription",
                                                  "aymara_preprocessed.txt"]))

    # Aymara sounds
    ## Unigrams
    plain_stops = "ptckq"
    aspirates = "PTCKQ"
    ejectives = "bdzgG"
    stops = plain_stops + aspirates + ejectives
    fricatives = "sShx"
    sonorants = "mnNrlYjw"
    consonants = stops + fricatives + sonorants
    vowels = "aAeEiIoOuU"
    sounds = vowels + consonants
    non_stops = "".join([sound for sound in sounds if sound not in stops])

    ## Multigrams
    precon_stops = {stop + consonant for stop in stops for consonant in consonants}
    prevoc_stops = {stop + vowel for stop in stops for vowel in vowels}
    stop_v_stop = {stop + vowel + stop for stop in stops for vowel in vowels}


    # Counting
    ## Stops
    unigram_counts = count_many_substr(sounds, ay_words)
    unigram_counts["stops"] = sum(unigram_counts[key] for key in stops)
    unigram_counts["plain_stops"] = sum(unigram_counts[key] for key in plain_stops)
    unigram_counts["aspirates"] = sum(unigram_counts[key] for key in aspirates)
    unigram_counts["ejectives"] = sum(unigram_counts[key] for key in ejectives)
    unigram_counts["consonants"] = sum(unigram_counts[key] for key in consonants)
    unigram_counts["vowels"] = sum(unigram_counts[key] for key in vowels)
    unigram_counts["total"] = sum(unigram_counts.values())

    write_dict(unigram_counts, os.path.join(*["Outputs",
                                           "Counts",
                                           "aymara_counts_stops.txt"]))


    ## Preceding environments for stops
    precon_stop_counts = count_many_substr(precon_stops, ay_words)
    prevoc_stop_counts = count_many_substr(prevoc_stops, ay_words)
    prec_env_stop_counts = {
        "preconsonantal stops": sum(precon_stop_counts.values()),
        "prevocalic stops": sum(prevoc_stop_counts.values()),
        "total stops": sum(precon_stop_counts.values()) + sum(prevoc_stop_counts.values())
    }

    write_dict(prec_env_stop_counts, os.path.join(*["Outputs",
                                                    "Counts",
                                                    "aymara_counts_stop_env.txt"]))


    # Prevocalic stops initially or not
    prevoc_stop_initial_counts = count_many_substr(prevoc_stops, ay_words, initial=True)
    prevoc_counts_wordpos = {
        "initial": sum(prevoc_stop_initial_counts.values()),
        "medial": sum(prevoc_stop_counts.values()) - sum(prevoc_stop_initial_counts.values()),
        "total": sum(prevoc_stop_counts.values())
    }

    write_dict(prevoc_counts_wordpos, os.path.join(*["Outputs",
                                                     "Counts",
                                                     "aymara_counts_prevoc_stop_wordpos.txt"]))


    # S ... S and SVS (S = stop, V = vowel)
    svs_counts = count_many_substr(stop_v_stop, ay_words)
    stop_x_stop = count_regexp(r"[{0}][{1}]*[{0}]".format(stops,non_stops), ay_words)

    stop_x_stop = {
        "stop vowel stop": sum(svs_counts.values()),
        "stop anything stop": stop_x_stop
    }

    write_dict(stop_x_stop, os.path.join(*["Outputs",
                                           "Counts",
                                           "aymara_counts_stop_x_stop.txt"]))



if __name__ == "__main__":
    main()
