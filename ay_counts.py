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
    precon_asp = {aspirate + consonant for aspirate in aspirates for consonant in consonants}
    precon_ej = {ejective + consonant for ejective in ejectives for consonant in consonants}
    precon_plain = {plain + consonant for plain in plain_stops for consonant in consonants}
    precon_stops = precon_asp.union(precon_ej, precon_plain)
    prevoc_asp = {aspirate + vowel for aspirate in aspirates for vowel in vowels}
    prevoc_ej = {ejective + vowel for ejective in ejectives for vowel in vowels}
    prevoc_plain = {plain + vowel for plain in plain_stops for vowel in vowels}
    prevoc_stops = prevoc_asp.union(prevoc_ej, prevoc_plain)

    stop_v_stop = {stop + vowel + stop for stop in stops for vowel in vowels}
    asp_v_asp = {a + v + a for a in aspirates for v in vowels}
    asp_v_ej = {a + v + e for a in aspirates for v in vowels for e in ejectives}
    asp_v_plain = {a + v + p for a in aspirates for v in vowels for p in plain_stops}
    ej_v_asp = {e + v + a for e in ejectives for v in vowels for a in aspirates}
    ej_v_ej = {e + v + e for e in ejectives for v in vowels}
    ej_v_plain = {e + v + p for e in ejectives for v in vowels for p in plain_stops}
    plain_v_asp = {p + v + a for p in plain_stops for v in vowels for a in aspirates}
    plain_v_ej = {p + v + e for p in plain_stops for v in vowels for e in ejectives}
    plain_v_plain = {p + v + p for p in plain_stops for v in vowels}


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
                                           "aymara_counts_unigrams.txt"]))


    ## Preceding environments for stops
    precon_stop_counts = count_many_substr(precon_stops, ay_words)
    prevoc_stop_counts = count_many_substr(prevoc_stops, ay_words)
    stop_bigrams = {
        "preconsonantal stops": sum(precon_stop_counts.values()),
        "prevocalic stops": sum(prevoc_stop_counts.values()),
        "total non-final stops": sum(precon_stop_counts.values()) + sum(prevoc_stop_counts.values())
    }

    stop_bigrams["preconsonantal aspirates"] \
        = sum(precon_stop_counts[key] for key in precon_asp)
    stop_bigrams["preconsonantal ejectives"] \
        = sum(precon_stop_counts[key] for key in precon_ej)
    stop_bigrams["preconsonantal plain stops"] \
        = sum(precon_stop_counts[key] for key in precon_plain)
    stop_bigrams["prevocalic aspirates"] \
        = sum(prevoc_stop_counts[key] for key in prevoc_asp)
    stop_bigrams["prevocalic ejectives"] \
        = sum(prevoc_stop_counts[key] for key in prevoc_ej)
    stop_bigrams["prevocalic plain stops"] \
        = sum(prevoc_stop_counts[key] for key in prevoc_plain)

    write_dict(stop_bigrams, os.path.join(*["Outputs",
                                            "Counts",
                                            "aymara_counts_stop_env.txt"]))


    # Prevocalic stops initially or not
    prevoc_stop_initial_counts = count_many_substr(prevoc_stops, ay_words, initial=True)
    prevoc_counts_wordpos = {
        "initial prevocalic stops": sum(prevoc_stop_initial_counts.values()),
        "medial prevocalic stops": sum(prevoc_stop_counts.values()) -
                                   sum(prevoc_stop_initial_counts.values()),
        "total prevocalic stops": sum(prevoc_stop_counts.values()),
        "initial prevocalic aspirates": sum(prevoc_stop_initial_counts[key] for key in prevoc_asp),
        "medial prevocialic aspirates": sum(prevoc_stop_counts[key] for key in prevoc_asp) -
                            sum(prevoc_stop_initial_counts[key] for key in prevoc_asp),
        "total prevocalic aspirates": sum(prevoc_stop_counts[key] for key in prevoc_asp),
        "initial prevocalic ejectives": sum(prevoc_stop_initial_counts[key] for key in prevoc_ej),
        "medial prevocalic ejectives": sum(prevoc_stop_counts[key] for key in prevoc_ej) -
                            sum(prevoc_stop_initial_counts[key] for key in prevoc_ej),
        "total prevocalic ejectives": sum(prevoc_stop_counts[key] for key in prevoc_ej),
        "initial prevocalic plain stops": sum(prevoc_stop_initial_counts[key] for key in prevoc_plain),
        "medial prevocalic plain stops": sum(prevoc_stop_counts[key] for key in prevoc_plain) -
                            sum(prevoc_stop_initial_counts[key] for key in prevoc_plain),
        "total prevocalic plain stops": sum(prevoc_stop_counts[key] for key in prevoc_plain)
    }

    write_dict(prevoc_counts_wordpos, os.path.join(*["Outputs",
                                                     "Counts",
                                                     "aymara_counts_prevoc_stop_wordpos.txt"]))


    # S ... S and SVS (S = stop, V = vowel)
    svs_counts = count_many_substr(stop_v_stop, ay_words)
    stop_x_stop = count_regexp(r"[{0}][{1}]*[{0}]".format(stops, non_stops), ay_words)
    asp_x_asp = \
        count_regexp(r"[{0}][{1}]*[{0}]".format(aspirates, non_stops), ay_words)
    asp_x_ej = \
        count_regexp(r"[{0}][{1}]*[{2}]".format(aspirates, non_stops, ejectives), ay_words)
    asp_x_plain = \
        count_regexp(r"[{0}][{1}]*[{2}]".format(aspirates, non_stops, plain_stops), ay_words)
    ej_x_asp = \
        count_regexp(r"[{0}][{1}]*[{2}]".format(ejectives, non_stops, aspirates), ay_words)
    ej_x_ej = \
        count_regexp(r"[{0}][{1}]*[{0}]".format(ejectives, non_stops), ay_words)
    ej_x_plain = \
        count_regexp(r"[{0}][{1}]*[{2}]".format(ejectives, non_stops, plain_stops), ay_words)
    plain_x_asp = \
        count_regexp(r"[{0}][{1}]*[{2}]".format(plain_stops, non_stops, aspirates), ay_words)
    plain_x_ej = \
        count_regexp(r"[{0}][{1}]*[{2}]".format(plain_stops, non_stops, ejectives), ay_words)
    plain_x_plain = \
        count_regexp(r"[{0}][{1}]*[{0}]".format(plain_stops, non_stops), ay_words)

    stop_x_stop = {
        "stop vowel stop": sum(svs_counts.values()),
        "aspirate vowel aspirate": sum(svs_counts[key] for key in svs_counts
                                       if key in asp_v_asp),
        "aspirate vowel ejective": sum(svs_counts[key] for key in svs_counts
                                       if key in asp_v_ej),
        "aspirate vowel plain stop": sum(svs_counts[key] for key in svs_counts
                                         if key in asp_v_plain),
        "ejective vowel aspirate": sum(svs_counts[key] for key in svs_counts
                                       if key in ej_v_asp),
        "ejective vowel ejective": sum(svs_counts[key] for key in svs_counts
                                       if key in ej_v_ej),
        "ejective vowel plain stop": sum(svs_counts[key] for key in svs_counts
                                         if key in ej_v_plain),
        "plain stop vowel aspirate": sum(svs_counts[key] for key in svs_counts
                                         if key in plain_v_asp),
        "plain stop vowel ejective": sum(svs_counts[key] for key in svs_counts
                                         if key in plain_v_ej),
        "plain stop vowel plain stop": sum(svs_counts[key] for key in svs_counts
                                           if key in plain_v_plain),
        "stop anything stop": stop_x_stop,
        "aspirate anything aspirate": asp_x_asp,
        "aspirate anything ejective": asp_x_ej,
        "aspirate anything plain stop": asp_x_plain,
        "ejective anything aspirate": ej_x_asp,
        "ejective anything ejective": ej_x_ej,
        "ejective anything plain stop": ej_x_plain,
        "plain stop anything aspirate": plain_x_asp,
        "plain stop anything ejective": plain_x_ej,
        "plain stop anything plain stop": plain_x_plain
    }

    write_dict(stop_x_stop, os.path.join(*["Outputs",
                                           "Counts",
                                           "aymara_counts_stop_x_stop.txt"]))



if __name__ == "__main__":
    main()
