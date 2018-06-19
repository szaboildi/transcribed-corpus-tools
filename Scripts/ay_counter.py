#!/usr/bin/python
import ay_transcriber as ay_trans
import ay_sp_en_filter as ay_filter
from languages import aymara as ay
import os


#######################
# Counting substrings #
#######################
## Mapping a string/word to a tier where it only contains characters of a substring
def map_tier(tier, word):
    """
    Maps a string to contain only a certain set of character
    :param tier: characters to map string to (ones that can remain) concatenated
    :param word: String to transcribe
    :return: Transcribed string
    """
    trans_word = ''
    for c in word:
        if c in tier:
            trans_word += c

    return trans_word


## Counting the occurences of a substring in a set of words (corpus)
def count_substr(substr, words, tier='', return_set=False):
    """
    Count the number of occurences of a substring in a set of words
    :param substr: substr to count
    :param words: set of words to count substr in
    :param tier: characters to map string to (ones that can remain) concatenated
                 allows for non-adjacent matches (intervening segments)
                 default: empty string
    :param return_set: whether it should return the set of hits
                       default: False
    :return: the number of occurrences of substr in st
             optionally the set of hits as well
    """
    if tier != '':
        subset = {item for item in words if substr in map_tier(tier, item)}
    else:
        subset = {item for item in words if substr in item}
    counter = 0

    for item in subset:
        if tier != '':
            trans_item = map_tier(tier, item)
            counter += trans_item.count(substr)
        else:
            counter += item.count(substr)

    if return_set:
        return subset, counter
    return counter


## Counting one substring word-initially
def count_initial_substr(substr, words, tier='', return_set=False):
    """
    Count the number of occurences of a substring in a set of words,
    where the substring is word-initial
    :param substr: substr to count
    :param words: set of words to count substr in
    :param tier: characters to map string to (ones that can remain) concatenated
                 allows for non-adjacent matches (intervening segments)
                 default: empty string
    :param return_set: whether it should return the set of hits
                       default: False
    :return: the number of occurrences of substr in st
    """
    if tier != '':
        subset = {item for item in words if
                  map_tier(tier, item).startswith(substr) and
                  substr[0] == item[0]}
    else:
        subset = {item for item in words if item.startswith(substr)}

    if return_set:
        return subset, len(subset)
    return len(subset)


## Counting many substrings (initial or any)
def count_many_substr(substrings, words, tier='', initial=False,
                      return_set=False):
    """
    Count the number of occurences of multiple substrings in a set of words
    Can count only initial occurences or not
    :param substrings: set of substrings to count
    :param words: set of words to count them in
    :param tier: characters to map string to (ones that can remain) concatenated
                 allows for non-adjacent matches (intervening segments)
                 default: empty string
    :param initial: if the substring has to be initial, default False
    :param return_set: whether it should return the set of hits
                       default: False
    :return: dictionary of counts, where keys are the counted substrings,
    and values are their respective counts.
    """
    hits = {}
    counts = {}
    for substr in substrings:
        if initial:
            result = count_initial_substr(substr, words, tier=tier,
                                         return_set=return_set)
        else:
            result = count_substr(substr, words, tier=tier,
                                 return_set=return_set)

        if return_set:
            hits[substr] = result[0]
            counts[substr] = result[1]
        else:
            counts[substr] = result

    if return_set:
        return hits, counts
    return counts



## Class for hits for substrings
class Hits_for_substring:
    def __init__(self, key_name, substrings, hitlist, counts):
        self.key_name = key_name
        self.matched_substrs = substrings
        self.hitlist = hitlist
        self.counts = counts


    def write_hitlist(self, path):
        """
        Writes out the hitlist into a file
        :param path: Where to write file to
        :return: None
        """
        hitset = [hit for hitlst in self.hitlist.values()
                  for hit in hitlst]

        ay_filter.write_iter(hitset, path)


    def sum_add_to_countdict(self, count_dict):
        """
        Adds count from this object to a dictionary
        :param count_dict: Dictionary to which to add count from this object
        :return: None, modifies dictionary in place
        """
        count_dict[self.key_name] = sum(self.counts.values())


"""
## Regular expressions:
def count_regexp(regexp, words, return_set=False):

    Count words matching a regular expression pattern in a set of words
    :param regexp: Regular expression to be matched
    :param words: Set of words to search in
    :param return_set: If it should return the set of matches as well
                       default: False
    :return: Number of matching words, optionally the words themselves too

    subset = set(filter(lambda s: re.match(regexp, s), words))

    if return_set:
        return subset, len(subset)
    return len(subset)
"""


####################
# Write dictionary #
####################
def write_dict(dict, path):
    """
    Writes dictionary into text file
    :param dict: dictionary to be written into file
    :param path: path of file to be written to
    :return: None
    """
    with open(path, 'w', encoding='utf-8') as output_w:
        for key in dict.keys():
            output_w.write('{}\t{}\n'.format(key, int(dict[key])))



def main():
    ay_words = ay_trans.set_reader(os.path.join(*[os.pardir,
                                                  'Outputs',
                                                  'Transcription',
                                                  'aymara_preprocessed.txt']))

    # Aymara sounds
    ## Unigrams
    """
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
    """

    ## Multigrams
    precon_asp = {aspirate + consonant for aspirate in ay.aspirates for consonant in ay.consonants}
    precon_ej = {ejective + consonant for ejective in ay.ejectives for consonant in ay.consonants}
    precon_plain = {plain + consonant for plain in ay.plain_stops for consonant in ay.consonants}
    precon_stops = precon_asp.union(precon_ej, precon_plain)
    prevoc_asp = {aspirate + vowel for aspirate in ay.aspirates for vowel in ay.vowels}
    prevoc_ej = {ejective + vowel for ejective in ay.ejectives for vowel in ay.vowels}
    prevoc_plain = {plain + vowel for plain in ay.plain_stops for vowel in ay.vowels}
    prevoc_stops = prevoc_asp.union(prevoc_ej, prevoc_plain)

    stop_v_stop = {stop1 + vowel + stop2
                   for stop1 in ay.stops for vowel in ay.vowels for stop2 in ay.stops}
    asp_v_asp = {a1 + v + a2 for a1 in ay.aspirates for v in ay.vowels for a2 in ay.aspirates}
    asp_v_ej = {a + v + e for a in ay.aspirates for v in ay.vowels for e in ay.ejectives}
    asp_v_plain = {a + v + p for a in ay.aspirates for v in ay.vowels for p in ay.plain_stops}
    ej_v_asp = {e + v + a for e in ay.ejectives for v in ay.vowels for a in ay.aspirates}
    ej_v_ej = {e1 + v + e2 for e1 in ay.ejectives for v in ay.vowels for e2 in ay.ejectives}
    ej_v_plain = {e + v + p for e in ay.ejectives for v in ay.vowels for p in ay.plain_stops}
    plain_v_asp = {p + v + a for p in ay.plain_stops for v in ay.vowels for a in ay.aspirates}
    plain_v_ej = {p + v + e for p in ay.plain_stops for v in ay.vowels for e in ay.ejectives}
    plain_v_plain = {p1 + v + p2 for p1 in ay.plain_stops for v in ay.vowels for p2 in ay.plain_stops}


    # Counting
    ## Stops
    unigram_counts = count_many_substr(ay.sounds, ay_words)
    unigram_counts['stops'] = sum(unigram_counts[key] for key in ay.stops)
    unigram_counts['plain_stops'] = sum(unigram_counts[key] for key in ay.plain_stops)
    unigram_counts['aspirates'] = sum(unigram_counts[key] for key in ay.aspirates)
    unigram_counts['ejectives'] = sum(unigram_counts[key] for key in ay.ejectives)
    unigram_counts['consonants'] = sum(unigram_counts[key] for key in ay.consonants)
    unigram_counts['vowels'] = sum(unigram_counts[key] for key in ay.vowels)
    unigram_counts['total'] = sum(unigram_counts.values())

    write_dict(unigram_counts, os.path.join(*[os.pardir,
                                              'Outputs',
                                              'Counts',
                                              'Raw',
                                              'aymara_counts_unigrams.txt']))


    ## Preceding environments for stops
    precon_stop_counts = count_many_substr(precon_stops, ay_words)
    prevoc_stop_counts = count_many_substr(prevoc_stops, ay_words)
    stop_bigrams = {
        'preconsonantal stops': sum(precon_stop_counts.values()),
        'prevocalic stops': sum(prevoc_stop_counts.values()),
        'total non-final stops': sum(precon_stop_counts.values()) + sum(prevoc_stop_counts.values())
    }

    stop_bigrams['preconsonantal aspirates'] \
        = sum(precon_stop_counts[key] for key in precon_asp)
    stop_bigrams['preconsonantal ejectives'] \
        = sum(precon_stop_counts[key] for key in precon_ej)
    stop_bigrams['preconsonantal plain stops'] \
        = sum(precon_stop_counts[key] for key in precon_plain)
    stop_bigrams['prevocalic aspirates'] \
        = sum(prevoc_stop_counts[key] for key in prevoc_asp)
    stop_bigrams['prevocalic ejectives'] \
        = sum(prevoc_stop_counts[key] for key in prevoc_ej)
    stop_bigrams['prevocalic plain stops'] \
        = sum(prevoc_stop_counts[key] for key in prevoc_plain)

    write_dict(stop_bigrams, os.path.join(*[os.pardir,
                                            'Outputs',
                                            'Counts',
                                            'Raw',
                                            'aymara_counts_stop_env.txt']))


    ## Prevocalic stops initially or not
    prevoc_stop_initial_counts = count_many_substr(prevoc_stops, ay_words, initial=True)
    prevoc_counts_wordpos = {
        'initial prevocalic stops': sum(prevoc_stop_initial_counts.values()),
        'medial prevocalic stops': sum(prevoc_stop_counts.values()) -
                                   sum(prevoc_stop_initial_counts.values()),
        'total prevocalic stops': sum(prevoc_stop_counts.values()),
        'initial prevocalic aspirates': sum(prevoc_stop_initial_counts[key] for key in prevoc_asp),
        'medial prevocialic aspirates': sum(prevoc_stop_counts[key] for key in prevoc_asp) -
                            sum(prevoc_stop_initial_counts[key] for key in prevoc_asp),
        'total prevocalic aspirates': sum(prevoc_stop_counts[key] for key in prevoc_asp),
        'initial prevocalic ejectives': sum(prevoc_stop_initial_counts[key] for key in prevoc_ej),
        'medial prevocalic ejectives': sum(prevoc_stop_counts[key] for key in prevoc_ej) -
                            sum(prevoc_stop_initial_counts[key] for key in prevoc_ej),
        'total prevocalic ejectives': sum(prevoc_stop_counts[key] for key in prevoc_ej),
        'initial prevocalic plain stops': sum(prevoc_stop_initial_counts[key] for key in prevoc_plain),
        'medial prevocalic plain stops': sum(prevoc_stop_counts[key] for key in prevoc_plain) -
                            sum(prevoc_stop_initial_counts[key] for key in prevoc_plain),
        'total prevocalic plain stops': sum(prevoc_stop_counts[key] for key in prevoc_plain)
    }

    write_dict(prevoc_counts_wordpos, os.path.join(*[os.pardir,
                                                     'Outputs',
                                                     'Counts',
                                                     'Raw',
                                                     'aymara_counts_prevoc_stop_wordpos.txt']))


    ## S ... S and SVS (S = stop, V = vowel)
    svs_counts = count_many_substr(stop_v_stop, ay_words)
    svs_general = {s1 + ' vowel ' + s2 for s1 in ay.stops for s2 in ay.stops}
    svs_seg_counts = dict()
    for trigram in svs_general:
        svs_seg_counts[trigram] = sum(svs_counts[key] for key in svs_counts if
                                      trigram[0] == key[0] and trigram[-1] == key[-1])
    sxs_counts = {
        'stop vowel stop': sum(svs_counts.values()),
        'aspirate vowel aspirate': sum(svs_counts[key] for key in svs_counts
                                       if key in asp_v_asp),
        'aspirate vowel ejective': sum(svs_counts[key] for key in svs_counts
                                       if key in asp_v_ej),
        'aspirate vowel plain stop': sum(svs_counts[key] for key in svs_counts
                                         if key in asp_v_plain),
        'ejective vowel aspirate': sum(svs_counts[key] for key in svs_counts
                                       if key in ej_v_asp),
        'ejective vowel ejective': sum(svs_counts[key] for key in svs_counts
                                       if key in ej_v_ej),
        'ejective vowel plain stop': sum(svs_counts[key] for key in svs_counts
                                         if key in ej_v_plain),
        'plain stop vowel aspirate': sum(svs_counts[key] for key in svs_counts
                                         if key in plain_v_asp),
        'plain stop vowel ejective': sum(svs_counts[key] for key in svs_counts
                                         if key in plain_v_ej),
        'plain stop vowel plain stop': sum(svs_counts[key] for key in svs_counts
                                           if key in plain_v_plain)
    }

    sxs_seg_hitlist, sxs_seg_counts = count_many_substr(
        {stop1 + stop2 for stop1 in ay.stops for stop2 in ay.stops},
        ay_words, tier=ay.stops, return_set=True)
    sxs_seg_counts_formatted = {key[0] + ' anything ' + key[1]: sxs_seg_counts[key]
                                for key in sxs_seg_counts.keys()}
    sxs = Hits_for_substring(
        substrings={s1 + s2 for s1 in ay.stops for s2 in ay.stops},
        key_name='stop anything stop',
        hitlist=sxs_seg_hitlist,
        counts=sxs_seg_counts_formatted
    )

    sxs.sum_add_to_countdict(sxs_counts)
    # sxs_hitlist = {sxs_seg_hitlist[key] for key in sxs_seg_hitlist.keys()}

    variable_names = ['axa', 'axe', 'axp', 'exa', 'exe',
                      'exp', 'pxa', 'pxe', 'pxp']
    key_names = [
        'aspirate anything aspirate', 'aspirate anything ejective',
        'aspirate anything plain stop', 'ejective anything aspirate',
        'ejective anything ejective', 'ejective anything plain stop',
        'plain stop anything aspirate', 'plain stop anything ejective',
        'plain stop anything plain stop'
    ]
    sets_of_substrings = [
        (ay.aspirates, ay.aspirates), (ay.aspirates, ay.ejectives), (ay.aspirates, ay.plain_stops),
        (ay.ejectives, ay.aspirates), (ay.ejectives, ay.ejectives), (ay.ejectives, ay.plain_stops),
        (ay.plain_stops, ay.aspirates), (ay.plain_stops, ay.ejectives), (ay.plain_stops, ay.plain_stops)
    ]

    for i, name in enumerate(variable_names):
        matched_substrings = {x + y
                              for x in sets_of_substrings[i][0]
                              for y in sets_of_substrings[i][1]}
        name = \
            Hits_for_substring(substrings=matched_substrings,
                               key_name=key_names[i],
                               hitlist={key: sxs_seg_hitlist[key]
                                        for key in sxs.hitlist.keys()
                                        if key in matched_substrings},
                               counts={key: sxs_seg_counts[key]
                                      for key in sxs_seg_counts.keys()
                                      if key in matched_substrings})

        name.sum_add_to_countdict(sxs_counts)
        name.write_hitlist(os.path.join(*[os.pardir,
                                          'Outputs',
                                          'Counts',
                                          'Lists',
                                          'aymara_list_{}.txt'
                                        .format(variable_names[i])]))

    write_dict(sxs_counts, os.path.join(*[os.pardir,
                                          'Outputs',
                                          'Counts',
                                          'Raw',
                                          'aymara_counts_class_stop_x_stop.txt']))

    write_dict(sxs_seg_counts_formatted, os.path.join(*[os.pardir,
                                                        'Outputs',
                                                        'Counts',
                                                        'Raw',
                                                        'aymara_counts_seg_stop_x_stop.txt']))

    write_dict(svs_seg_counts, os.path.join(*[os.pardir,
                                              'Outputs',
                                              'Counts',
                                              'Raw',
                                              'aymara_counts_seg_stop_v_stop.txt']))


if __name__ == '__main__':
    main()
