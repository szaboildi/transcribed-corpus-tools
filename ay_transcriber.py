#!/usr/bin/python
import itertools


############################
# Reading in the word list #
############################
def list_reader(filename):
    """
    Reads in file into list.
    :param filename: location of text file with one word/line
    :return: a list of words
    """
    lst = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            word = word.lower()
            if word.isalpha() and word not in lst:
                lst.append(word)

    return lst


##############################################
# Implementing pronunciation rules in Aymara #
##############################################
def transcribe(lst):
    """
    Transcribes a list of words into a pre-processed list
    that reflects pronunciation in a pseudo-transcription.
    :param lst: input list
    :return: output list
    """
    out_lst = []

    # Orthography:
    ## V length
    vowel_len = {u"ä": u"A",
                 u"ü": u"U",
                 u"ï": u"I"}
    ## ch -> c
    ## ñ -> N
    ## j -> h
    trans1 = {u"ch": u"c",
              u"ñ": u"N",
              u"j": u"H"}
    ## y -> j
    trans2 = {u"y": u"j",
              u"h": u"H"}
    ## ll -> alveo-palatal lateral (encoded as Y)
    trans3 = {u"ll": u"Y"}

    # Rule 1 (Frication): ch -> s/S before /t/
    frication = {u"ct": u"st"}

    # Rule 2 (Sibilant place): S after ch-series, y and N
    sib_pl = {u"cs": u"cS",
              u"ys": u"yS",
              u"Ns": u"NS"}

    # Rule 3 (V height): u, U, i, I lower around q series and x
    lowering_env = [u"q", u"q'", u"qh", u"x"]
    lowering_v = [u"u", u"U", u"i", u"I"]
    v_pairs = {u"u": u"o",
               u"U": u"O",
               u"i": u"e",
               u"I": u"E"}
    lowering_bigrams = itertools.product(lowering_env, lowering_v) + \
                       itertools.product(lowering_v, lowering_env)
    lowering = {}
    for bg in lowering_bigrams:
        lowering[lowering_bigrams] = lowering_bigrams.replace(v_pairs)


    for wrd in lst:
        # Orthography
        wrd = wrd.replace(vowel_len)
        wrd = wrd.replace(trans1)
        wrd = wrd.replace(trans2)
        wrd = wrd.replace(trans3)

        # Rule 1 (Frication)
        wrd = wrd.replace(frication)
        # Rule 2 (Sibilant place)
        wrd = wrd.replace(sib_pl)
        # Rule 3 (Vowel height)
        wrd = wrd.replace(lowering)

        # Appends word to the final list
        if wrd not in out_lst:
            out_lst.append(wrd)

    return out_lst


def ipa_trans(lst):
    """
    Transcribes a list of words into IPA and writes it to file
    :param lst: input list of preprocessed words
    :return: None
    """
    ipa_lst = []

    # write rules that actually make IPA changes:
    # ipa_trans = {}
    ## c -> tS
    ## S -> S
    ## aspiration?
    ## Y -> lambda
    ## V length (uppercase = long)
    ## N -> ñ

    for wrd in lst:

        if wrd not in ipa_lst:
            ipa_lst.append(wrd)


    return ipa_lst


def pl_trans(lst):
    """
    Transcribes a list of words in the style of the UCLA
    Phonotactic Learner and writes it to file
    :param lst: input list of preprocessed words
    :return: None
    """




def main():
    ay_orth = list_reader("Outputs\\Aymara_words_no_sp_en.txt")
    ay_trans = transcribe(ay_orth)