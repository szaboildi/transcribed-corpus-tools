#!/usr/bin/python
import itertools
import ay_sp_en_filter as ay


############################
# Reading in the word list #
############################
def list_reader(path):
    """
    Reads in file into list.
    :param path: location of text file with one word/line
    :return: a list of words
    """
    lst = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            word = word.lower()
            if word not in lst:
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

    trans1 = {
        ## ch -> c
        u"ch": u"c",
        ## ñ -> N
        u"ñ": u"N",
        ## j -> h
        u"j": u"H",
        ## V length
        u"ä": u"A",
        u"ü": u"U",
        u"ï": u"I",
        ## ll -> alveo-palatal lateral (encoded as Y)
        u"ll": u"Y"
    }

    trans2 = {
        ## y -> j
        u"y": u"j",
        u"h": u"H",
        ## aspiration
        u"ph": u"P",
        u"th": u"T",
        u"ch": u"C",
        u"kh": u"K",
        u"qh": u"Q",
        ## ejectives
        u"p'": u"b",
        u"t'": u"d",
        u"c'": u"z",
        u"k'": u"g",
        u"q'": u"G"
    }


    rules = {
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

    # Rule 3 (V height): u, U, i, I lower around q series and x
    lowering_env = [u"q", u"Q", u"G", u"x"]
    lowering_v = [u"u", u"U", u"i", u"I"]
    v_pairs = {u"u": u"o",
               u"U": u"O",
               u"i": u"e",
               u"I": u"E"}

    lowering_bigrams = list(itertools.product(lowering_env, lowering_v))
    lowering_bigrams.extend(list(itertools.product(lowering_v, lowering_env)))

    lowering = {}
    for bg in lowering_bigrams:
        bg_str = "".join(bg)
        lowering[bg_str] = bg_str.translate(v_pairs)


    for wrd in lst:
        # Orthography
        wrd = wrd.translate(trans1)
        wrd = wrd.translate(trans2)

        # Rule 1 (Frication) & Rule 2 (Sibilant place)
        wrd = wrd.translate(rules)
        # Rule 3 (Vowel height)
        wrd = wrd.translate(lowering)

        # Appends word to the final list
        if wrd not in out_lst:
            out_lst.append(wrd)

    return out_lst



############################################
# Transcribing preprocessed words into IPA #
############################################
def ipa_trans(lst):
    """
    Transcribes a list of words into IPA
    :param lst: input list of preprocessed words
    :return: ipa_lst, a list of words in IPA
    """
    ipa_lst = []

    # write rules that actually make IPA changes:
    ## c -> tS
    ## S -> S
    ## Y -> alveopalatal lateral
    ## N -> ñ
    ## V length (uppercase = long)
    ipa_pairs = {u"c":u"ʧ",
                 u"S":u"ʃ",
                 u"Y":u"ʎ",
                 u"N":u"ñ",
                 u"A":u"aː",
                 u"E": u"eː",
                 u"I": u"iː",
                 u"O": u"oː",
                 u"U": u"uː",
                 u"P": u"ph",
                 u"T": u"th",
                 u"C": u"ʧh",
                 u"K": u"kh",
                 u"Q": u"qh",
                 u"b": u"p'",
                 u"d": u"t'",
                 u"z": u"ʧ'",
                 u"g": u"k'",
                 u"G": u"q'"}

    for wrd in lst:
        wrd = wrd.translate(ipa_pairs)
        if wrd not in ipa_lst:
            ipa_lst.append(wrd)

    return ipa_lst



###############################################
# Transcribing preprocessed words for UCLA PL #
###############################################
def pl_trans(lst):
    """
    Transcribes a list of words in the style of the UCLA Phonotactic Learner
    :param lst: input list of preprocessed words
    :return: pl_lst a list of UCLA PL-compatible words
    """
    pl_lst = []
    for wrd in lst:
        # wrd = wrd.replace(word, str(word))
        chars = list(wrd)
        pl_wrd = " ".join(chars)
        if pl_wrd not in pl_lst:
            pl_lst.append(pl_wrd)

    return pl_lst


def main():
    ay_orth = list_reader("Outputs\\Aymara_words_no_sp_en.txt")
    ay_trans = transcribe(ay_orth)

    ay_ipa = ipa_trans(ay_trans)
    ay.write_list(ay_ipa, "Outputs\\aymara_ipa.txt")

    ay_pl = pl_trans(ay_trans)
    ay.write_list(ay_pl, "Outputs\\aymara_pl.txt")


if __name__ == "__main__":
    main()