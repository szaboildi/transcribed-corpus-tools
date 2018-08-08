#!/usr/bin/python

"""
Copyright (C) 2018 Ildiko Emese Szabo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
############################################################
# Defines utility functions for counting ngrams in corpora #
############################################################

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


def map_onset(word, lang, vowels=False):
    """
    Maps a word to the consonants in it that precede a vowel
    (and optionally the vowels too)
    :param word: Word to be mapped
    :param lang: Language (to get vowels and consonants from)
    :param vowels: If the vowels should be included in the mapped word
                   default: False
    :return: Mapped word
    """
    mapped_word = ''
    for i, ch in enumerate(word):
        if ch != word[-1] and ch in lang.consonants and word[i+1] in lang.vowels:
            if vowels:
                mapped_word += ch + word[i+1]
            else:
                mapped_word += ch

    return mapped_word


## Counting the occurences of a substring in a set of words (corpus)
def count_substr(substr, words, lang, tier='',
                 onset=False, ons_vowel=False, return_set=False):
    """
    Count the number of occurences of a substring in a set of words
    :param substr: substr to count
    :param words: set of words to count substr in
    :param lang: language (to get consonants and vowels from)
    :param tier: characters to map string to (ones that can remain) concatenated
                 allows for non-adjacent matches (intervening segments)
                 default: empty string
    :param onset: if the pattern should only hold over onsets
                  default: False
    :param ons_vowel: (if onset is True) whether vowels should be
                      included in the mapping
                      default: False
    :param return_set: whether it should return the set of hits
                       default: False
    :return: the number of occurrences of substr in st
             optionally the set of hits as well
    """
    if tier != '' and onset:
        subset = {item for item in words if substr in
                  map_tier(tier, map_onset(item, lang, vowels=ons_vowel))}
    elif tier != '':
        subset = {item for item in words if substr in map_tier(tier, item)}
    elif onset:
        subset = {item for item in words if substr in
                  map_onset(item, lang, vowels=ons_vowel)}
    else:
        subset = {item for item in words if substr in item}
    counter = 0

    for item in subset:
        if onset:
            item = map_onset(item, lang)
        if tier != '':
            item = map_tier(tier, item)

        counter += item.count(substr)

    if return_set:
        return subset, counter
    return counter


## Counting one substring word-initially
def count_initial_substr(substr, words, lang, tier='',
                         onset=False, ons_vowel=False, return_set=False):
    """
    Count the number of occurences of a substring in a set of words,
    where the substring is word-initial
    :param substr: substr to count
    :param words: set of words to count substr in
    :param lang: language (to get consonants and vowels from)
    :param tier: characters to map string to (ones that can remain) concatenated
                 allows for non-adjacent matches (intervening segments)
                 default: empty string
    :param onset: if the pattern should only hold over onsets
                  default: False
    :param ons_vowel: (if onset is True) whether vowels should be
                      included in the mapping
                      default: False
    :param return_set: whether it should return the set of hits
                       default: False
    :return: the number of occurrences of substr in st
    """
    if tier != '' and onset:
        subset = {item for item in words if
                  map_tier(tier,  map_onset(item, lang, vowels=ons_vowel))
                      .startswith(substr) and substr[0] == item[0]}
    elif tier != '':
        subset = {item for item in words if
                  map_tier(tier, item)
                      .startswith(substr) and substr[0] == item[0]}
    elif onset:
        subset = {item for item in words if
                  map_onset(item, lang, vowels=ons_vowel)
                      .startswith(substr) and substr[0] == item[0]}
    else:
        subset = {item for item in words if item.startswith(substr)}

    if return_set:
        return subset, len(subset)
    return len(subset)


## Counting many substrings (initial or any)
def count_many_substr(substrings, words, lang, tier='', onset=False,
                      ons_vowel=False, initial=False, return_set=False):
    """
    Count the number of occurences of multiple substrings in a set of words
    Can count only initial occurences or not
    :param substrings: set of substrings to count
    :param words: set of words to count them in
    :param lang: language (to get consonants and vowels from)
    :param tier: characters to map string to (ones that can remain) concatenated
                 allows for non-adjacent matches (intervening segments)
                 default: empty string ('')
    :param onset: if the pattern should only hold over onsets
                  default: False
    :param ons_vowel: (if onset is True) whether vowels should be
                      included in the mapping
                      default: False
    :param initial: if the substring has to be initial, default False
    :param return_set: whether it should return the set of hits
                       default: False
    :return: dictionary of counts, where keys are the counted substrings,
    and values are their respective counts. Optionally also returns a return set.
    """
    hits = {}
    counts = {}
    for substr in substrings:
        if initial:
            result = count_initial_substr(substr, words, lang, tier=tier,
                                          onset=onset, ons_vowel=ons_vowel,
                                          return_set=return_set)
        else:
            result = count_substr(substr, words, lang, tier=tier, onset=onset,
                                  ons_vowel=ons_vowel, return_set=return_set)

        if return_set:
            hits[substr] = result[0]
            counts[substr] = result[1]
        else:
            counts[substr] = result

    if return_set:
        return hits, counts
    return counts


# Counts all possible trigrams in the corpus
def trigram_counter(corpus):
    """
    Reads in corpus and countrs all trigrams in it,
    returns the resulting counts in a dictionary
    :param corpus: set of words to count trigrams in
    :return: dictionary of counts for each trigram
    """
    counts = dict()
    for word in corpus:
        for i in range(len(word) - 2):
            trigram = word[i:i+3]
            counts[trigram] = counts.get(trigram, 0) + 1

    return counts
