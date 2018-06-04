#!/usr/bin/python
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
    with open(path, 'r', encoding='utf-8') as f:
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
    repl = {
        ## ch -> c
        u"ch": u"c",
        ## ll -> alveo-palatal lateral (encoded as Y)
        u"ll": u"Y",
        ## aspiration
        u"ph": u"P",
        u"th": u"T",
        u"chh": u"C",
        u"kh": u"K",
        u"qh": u"Q",
        ## ejectives
        u"p'": u"b",
        u"t'": u"d",
        u"c'": u"z",
        u"k'": u"g",
        u"q'": u"G",
        # Rule 1 (Frication): ch -> s/S before /t/
        # if it happens before th and t' as well,
        # this needs to be moved into trans1
        u"ct": u"st",
        # Rule 2 (Sibilant place): S after ch-series, y and N
        # cannot be in or before trans1
        u"cs": u"cS",
        u"ys": u"yS",
        u"Ns": u"NS"
    }

    for bigram in repl:
        word = word.replace(bigram, repl[bigram])
    return word


## Rule 3 (V height): u, U, i, I lower around q series and x
def lower_vow(word):
    """

    Lowers any u and i in a word into o and e if it's in a lowering environment
    :param word: a word
    :return: the word after lowering applied
    """
    lowering_env = [u"q", u"Q", u"G", u"x"]
    lowering_v = [u"u", u"U", u"i", u"I"]
    v_pairs = {
        ord(u"u"): u"o",
        ord(u"U"): u"O",
        ord(u"i"): u"e",
        ord(u"I"): u"E"
    }

    lowering_bigrams = list(itertools.product(lowering_env, lowering_v))
    lowering_bigrams.extend(list(itertools.product(lowering_v, lowering_env)))

    lowering = {}
    for bg in lowering_bigrams:
        bg_str = "".join(bg)
        lowering[bg_str] = bg_str.translate(v_pairs)

    for vow_env in lowering:
        word = word.replace(vow_env, lowering[vow_env])
    return word


## Final transcription
def transcribe(st):
    """
    Transcribes a set of words into a pre-processed list
    that reflects pronunciation in a pseudo-transcription.
    :param st: input set
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
        ord(u"y"): u"j"
    }


    out_set = {lower_vow(bigram_repl(wrd.translate(trans1))) for wrd in st}
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
    ipa_pairs = {
        ## c -> ʧ
        ord(u"c"):u"ʧ",
        ## S -> ʃ
        ord(u"S"):u"ʃ",
        ## Y -> alveopalatal lateral
        ord(u"Y"):u"ʎ",
        ## N -> ñ
        ord(u"N"):u"ñ",
        ## Vowel length
        ord(u"A"):u"aː",
        ord(u"E"): u"eː",
        ord(u"I"): u"iː",
        ord(u"O"): u"oː",
        ord(u"U"): u"uː",
        ## Aspiration
        ord(u"P"): u"ph",
        ord(u"T"): u"th",
        ord(u"C"): u"ʧh",
        ord(u"K"): u"kh",
        ord(u"Q"): u"qh",
        ## Ejectives
        ord(u"b"): u"p'",
        ord(u"d"): u"t'",
        ord(u"z"): u"ʧ'",
        ord(u"g"): u"k'",
        ord(u"G"): u"q'"
    }

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
    ay_orth = set_reader(os.path.join("Outputs",
                                      "Aymara_words_no_sp_en.txt"))
    ay_trans = transcribe(ay_orth)
    ay.write_iter(ay_trans, os.path.join(*["Outputs",
                                           "Transcription",
                                           "aymara_preprocessed.txt"]))

    ay_ipa = ipa_trans(ay_trans)
    ay.write_iter(ay_ipa, os.path.join(*["Outputs",
                                         "Transcription",
                                         "aymara_ipa.txt"]))

    ay_pl = pl_trans(ay_trans)
    ay.write_iter(ay_pl, os.path.join(*["Outputs",
                                        "Transcription",
                                        "aymara_pl.txt"]))


if __name__ == "__main__":
    main()