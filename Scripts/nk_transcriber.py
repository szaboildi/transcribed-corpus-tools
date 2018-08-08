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

import os
import tct_utility as uti
from tct_languages import nkore_kiga as nk


def transcribe(st, palatalize=False):
    """
    Transcribes a set of Nkore-Kiga words with optional palatalization.
    :param st: Set of words to be transcribed (orthographic forms)
    :param palatalize: Whether to do palatalization on the words
                       Default: False
    :return: Transcribed set of words
    """
    trans_st = set()

    bi_repl1 = {}
    # Vowels
    bi_repl1.update({
        u'aa': u'A',
        u'ee': u'E',
        u'ii': u'I',
        u'oo': u'O',
        u'uu': u'U'
    })

    # Sibilants
    bi_repl1.update({
        u'sh': u'S',
        u'j': u'Z',
        u'c': u'T'
    })

    # Nasals
    bi_repl1.update({
        u'ny': u'Y',
        u'nk': u'Nk',
        u'ng': u'Ng',
        u'nn': u'n',
        u'mm': u'm'
    })

    # Clean-up
    bi_repl2 = {
        u'y':u'j'
    }

    for word in st:
        for bigram in bi_repl1:
            word = word.replace(bigram, bi_repl1[bigram])

        for bigram in bi_repl2:
            word = word.replace(bigram, bi_repl2[bigram])

        if palatalize:
            word = palatal_assim(word)

        trans_st.add(word)

    return trans_st


def palatal_assim(word):
    """
    Transcribes palatal assimilation for a Nkore-Kiga word
    :param word: Pre-processed word to perform palatal assimilation on.
    :return: Word after assimilation
    """
    # What happens with kI, ke, gI, ge?
    pal_dict = {
        u'ki': u'T',
        u'kI': u'Ti',
        u'kj': u'T',
        u'ky': u'T',
        u'gi': u'D',
        u'gj': u'D',
        u'gy': u'D',
        u'gI': u'Di'
    }

    for string in pal_dict:
        word = word.replace(string, pal_dict[string])

    return word


# Pre-nasal lengthening?
# Word-final, post w lengthening

def ipa_trans(st):
    """
    Transcribes a set of words into IPA
    :param st: input list of preprocessed words
    :return: ipa_set, a list of words in IPA
    """
    ipa_pairs = {}

    # Vowels
    ipa_pairs.update({
        ord(u'A'): u'aː',
        ord(u'E'): u'eː',
        ord(u'i'): u'ɪ',
        ord(u'I'): u'ɪː',
        ord(u'O'): u'oː',
        ord(u'U'): u'uː'
    })

    # Sibilants
    ipa_pairs.update({
        ord(u'T'): u'ʧ',
        ord(u'D'): u'ʤ',
        ord(u'S'): u'ʃ',
        ord(u'Z'): u'ʒ'
    })

    # Nasals
    ipa_pairs.update({
        ord(u'Y'): u'ɲ',
        ord(u'N'): u'ŋ'
    })

    ipa_set = {wrd.translate(ipa_pairs) for wrd in st}

    return ipa_set


def main():
    # Reading in files
    nk_orth_roots = uti.set_reader(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'nk_roots_pretrans.txt')))
    nk_orth_forms = uti.set_reader(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'nk_forms_pretrans.txt')))
    nk_orth_pars = uti.set_reader(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'nk_forms_sep_pretrans.txt')))

    # Transcribing & Writing
    # Roots
    nk_trans_roots = transcribe(nk_orth_roots, palatalize=True)
    uti.write_iter(nk_trans_roots, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'Preprocessed', 'nk_roots_preprocessed.txt')))
    nk_ipa_roots = ipa_trans(nk_trans_roots)
    uti.write_iter(nk_ipa_roots, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'IPA', 'nk_roots_ipa.txt')))
    nk_pl_roots = uti.pl_trans(nk_trans_roots)
    uti.write_iter(nk_pl_roots, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'UCLAPL', 'nk_roots_pl.txt')))

    # Word forms
    nk_trans_forms = transcribe(nk_orth_forms, palatalize=True)
    uti.write_iter(nk_trans_forms, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'Preprocessed', 'nk_forms_preprocessed.txt')))
    nk_ipa_forms = ipa_trans(nk_trans_forms)
    uti.write_iter(nk_ipa_forms, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'IPA', 'nk_forms_ipa.txt')))
    nk_pl_forms = uti.pl_trans(nk_trans_forms)
    uti.write_iter(nk_pl_forms, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'UCLAPL', 'nk_forms_pl.txt')))

    # Parsed word forms
    nk_trans_pars = transcribe(nk_orth_pars, palatalize=True)
    uti.write_iter(nk_trans_pars, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'Preprocessed', 'nk_forms_sep_preprocessed.txt')))
    nk_ipa_pars = ipa_trans(nk_trans_pars)
    uti.write_iter(nk_ipa_pars, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'IPA', 'nk_forms_sep_ipa.txt')))
    nk_pl_pars = uti.pl_trans(nk_trans_pars)
    uti.write_iter(nk_pl_pars, os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription',
        'UCLAPL', 'nk_forms_sep_pl.txt')))



if __name__ == '__main__':
    main()