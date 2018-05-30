#!/usr/bin/python
import itertools
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
        lst = {line.strip().lower() for line in f}

    return lst


##############################################
# Implementing pronunciation rules in Aymara #
##############################################
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
        u"ä": u"A",
        u"ü": u"U",
        u"ï": u"I",
        ## ch -> c
        u"ch": u"c",
        ## ñ -> N
        u"ñ": u"N",
        ## j -> h
        u"j": u"H",
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
    v_pairs = {
        u"u": u"o",
        u"U": u"O",
        u"i": u"e",
        u"I": u"E"
    }

    lowering_bigrams = list(itertools.product(lowering_env, lowering_v))
    lowering_bigrams.extend(list(itertools.product(lowering_v, lowering_env)))

    lowering = {}
    for bg in lowering_bigrams:
        bg_str = "".join(bg)
        lowering[bg_str] = bg_str.translate(v_pairs)

    out_set = {wrd.translate(trans1).translate(trans2).translate(rules).translate(lowering) for wrd in st}

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
        u"c":u"ʧ",
        ## S -> ʃ
        u"S":u"ʃ",
        ## Y -> alveopalatal lateral
        u"Y":u"ʎ",
        ## N -> ñ
        u"N":u"ñ",
        ## Vowel length
        u"A":u"aː",
        u"E": u"eː",
        u"I": u"iː",
        u"O": u"oː",
        u"U": u"uː",
        ## Aspiration
        u"P": u"ph",
        u"T": u"th",
        u"C": u"ʧh",
        u"K": u"kh",
        u"Q": u"qh",
        ## Ejectives
        u"b": u"p'",
        u"d": u"t'",
        u"z": u"ʧ'",
        u"g": u"k'",
        u"G": u"q'"
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
    ay_orth = set_reader("Outputs\\Aymara_words_no_sp_en.txt")
    ay_trans = transcribe(ay_orth)
    ay.write_iter(ay_trans, "Outputs\\aymara_preprocessed.txt")

    ay_ipa = ipa_trans(ay_trans)
    ay.write_iter(ay_ipa, "Outputs\\aymara_ipa.txt")

    ay_pl = pl_trans(ay_trans)
    ay.write_iter(ay_pl, "Outputs\\aymara_pl.txt")


if __name__ == "__main__":
    main()