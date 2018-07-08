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

import itertools
import os
import ay_sp_en_filter as ay

############################
# Reading in the word list #
############################
def set_reader(path):
    """
    Reads in file into a set.
    :param path: location of text file with one word/line
    :return: a set of words
    """
    with open(path, "r", encoding="utf-8") as f:
        lst = {line.strip() for line in f}

    return lst


##############################################
# Implementing pronunciation rules in Aymara #
##############################################
## Bigram replacements
def bigram_repl(word):
    """
    Makes the relevant bigram replacements in Aymara
    :param word: input word
    :return: word after the replacements
    """
    bi_repl1 = {}

    ## ch -> c
    bi_repl1.update({u"ch": u"c"})

    ## ll -> alveo-palatal lateral (encoded as Y)
    bi_repl1.update({u"ll": u"Y"})

    bi_repl2 = {}
    ## aspiration
    bi_repl2.update({
        u"ph": u"P",
        u"th": u"T",
        u"ch": u"C",
        u"kh": u"K",
        u"qh": u"Q"
    })

    ## ejectives
    bi_repl2.update({
        u"p'": u"b",
        u"t'": u"d",
        u"c'": u"z",
        u"k'": u"g",
        u"q'": u"G"
    })

    # Rule 2 (Sibilant place): S after ch-series, y and N
    # cannot be in or before trans1
    bi_repl3 = {}
    bi_repl3.update({
        u"cs": u"cS",
        u"Cs": u"CS",
        u"zs": u"zS",
        u"js": u"yS",
        u"Ns": u"NS"
    })

    for bigram in bi_repl1:
        word = word.replace(bigram, bi_repl1[bigram])

    for bigram in bi_repl2:
        word = word.replace(bigram, bi_repl2[bigram])

    for bigram in bi_repl3:
        word = word.replace(bigram, bi_repl3[bigram])

    return word


## Rule 3 (V height): u, U, i, I lower around q series and x
def make_lowering_table():
    """
    Makes a table of lowering, conditioned in certain environments 
    :return: None
    """
    lowering_env = u"qQGx"
    consonants = u"ptckqPTCKQbdzgGsShxmnNrlYjw"
    lowering_v = u"uUiI"
    v_pairs = {
        ord(u"u"): u"o",
        ord(u"U"): u"O",
        ord(u"i"): u"e",
        ord(u"I"): u"E"
    }

    lowering_strings = set(itertools.product(lowering_env, lowering_v))
    lowering_strings = lowering_strings.union(
        set(itertools.product(lowering_v, lowering_env)))
    lowering_strings = lowering_strings.union(
        set(itertools.product(lowering_env, consonants, lowering_v)))
    lowering_strings = lowering_strings.union(
        set(itertools.product(lowering_v, consonants, lowering_env)))

    lowering = {}
    for string in lowering_strings:
        gram_str = "".join(string)
        lowering[gram_str] = gram_str.translate(v_pairs)
    
    return lowering
    
    
def lower_vow(word, lowering):
    """

    Lowers any u and i in a word into o and e if it's in a lowering environment
    :param word: a word
    :param lowering: lowering replacements
    :return: the word after lowering applied
    """
    for vow_env in lowering:
        word = word.replace(vow_env, lowering[vow_env])

    return word


## Final transcription
def transcribe(st, lowering):
    """
    Transcribes a set of words into a pre-processed list
    that reflects pronunciation in a pseudo-transcription.
    :param st: input set
    :param lowering: set of lowering replacements
    :return: output set
    """

    # Orthography:
    trans1 = {
        ## V length
        ord(u"ä"): u"A",
        ord(u"ü"): u"U",
        ord(u"ï"): u"I",
        ## ñ -> N
        ord(u"ñ"): u"N",
        ## j -> h
        ord(u"j"): u"h",
        ## y -> j
        ord(u"y"): u"j",
        # Rule 1 (Frication): ch -> s/S before /t t' th/
        u"ct": u"st"
    }

    out_set = {lower_vow(bigram_repl(wrd.translate(trans1)), lowering=lowering) for wrd in st}
    out_set = {wrd for wrd in out_set if "'" not in wrd}

    return out_set



############################################
# Transcribing preprocessed words into IPA #
############################################
def ipa_trans(st):
    """
    Transcribes a set of words into IPA
    :param st: input list of preprocessed words
    :return: ipa_set, a list of words in IPA
    """
    ipa_pairs = {}

    ipa_pairs.update({
        ord(u"c"): u"ʧ",
        ord(u"S"): u"ʃ",
        ord(u"Y"):u"ʎ",
        ord(u"N"):u"ɲ"
    })

    ## Vowel length
    ipa_pairs.update({
        ord(u"A"):u"aː",
        ord(u"E"): u"eː",
        ord(u"I"): u"iː",
        ord(u"O"): u"oː",
        ord(u"U"): u"uː"
    })

    ## Aspiration
    ipa_pairs.update({
        ord(u"P"): u"ph",
        ord(u"T"): u"th",
        ord(u"C"): u"ʧh",
        ord(u"K"): u"kh",
        ord(u"Q"): u"qh"
    })

    ## Ejectives
    ipa_pairs.update({
        ord(u"b"): u"p'",
        ord(u"d"): u"t'",
        ord(u"z"): u"ʧ'",
        ord(u"g"): u"k'",
        ord(u"G"): u"q'"
    })

    ipa_set = {wrd.translate(ipa_pairs) for wrd in st}

    return ipa_set



###############################################
# Transcribing preprocessed words for UCLA PL #
###############################################
def pl_trans(st):
    """
    Transcribes a set of words in the style of the UCLA Phonotactic Learner
    :param st: input set of preprocessed words
    :return: pl_set a set of UCLA PL-compatible words
    """

    pl_set = {" ".join(list(wrd)) for wrd in st}

    return pl_set


def main():
    ay_orth = set_reader(os.path.join(*[os.pardir,
                                        "Outputs",
                                        "Aymara_words_no_sp_en.txt"]))
    
    lowering_table = make_lowering_table()
    ay_trans = transcribe(ay_orth, lowering=lowering_table)
    ay.write_iter(ay_trans, os.path.join(*[os.pardir,
                                           "Outputs",
                                           "Transcription",
                                           "aymara_preprocessed.txt"]))

    ay_ipa = ipa_trans(ay_trans)
    ay.write_iter(ay_ipa, os.path.join(*[os.pardir,
                                         "Outputs",
                                         "Transcription",
                                         "aymara_ipa.txt"]))

    ay_pl = pl_trans(ay_trans)
    ay.write_iter(ay_pl, os.path.join(*[os.pardir,
                                        "Outputs",
                                        "Transcription",
                                        "aymara_pl.txt"]))


if __name__ == "__main__":
    main()
