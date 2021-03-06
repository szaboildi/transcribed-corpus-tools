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

import tct_utility as uti
import ay_transcriber as ay_trans
from tct_languages import aymara as ay
import os


def delucca_reader(path):
    """
    Reads in the delucca corpus into a dictionary
    :param path: path of the delucca dictionary
    :return: set of suffixes, set of roots
    """
    roots = set()
    suffixes = set()

    with open(path, 'r', encoding='utf-8') as delucca_f:
        for line in delucca_f:
            if ' ' in line:
                continue
            morphs = line.strip().split('-')
            morphs = [m.replace('(', '').replace(')', '') for m in morphs]

            if morphs[0] not in roots:
                roots.add(morphs[0])

            # I don't need exception handling for iterating over a
            ## potentially empty list, right?
            for morph in morphs[1:]:
                if morph not in suffixes:
                    suffixes.add(morph)

    return roots, suffixes


def rid_of_starters(corpus, roots):
    """
    Filtering a corpus using a set of roots -- if a word starts with a root,
    it is deleted from the corpus
    :param corpus: Set of words to filter
    :param roots: List of roots to cross-check with
    :return: Subset of corpus
    """
    for root in roots:
        subcorpus = {wd for wd in corpus if not wd.startswith(root)}
        corpus = subcorpus

    return subcorpus


def first_n_syllables(word, n, lang):
    """
    Finds the first n syllables of a word.
    :param word: Word
    :param n: First how many syllables to look for
    :param lang: Language the word is in
    :return: The first n syllables of the word
    """
    syllables = ''
    counter = 0
    for i, ch in enumerate(word):
        syllables += ch
        if ch in lang.vowels:
            counter += 1
        try:
            if counter == 3:
                if syllables[-1] in lang.long_v:
                    syllables = syllables[:-1] + syllables[-1].lower()
                return syllables
        except IndexError:
            return word
    return word


def wd_stemmer(word, words, suffixes, lang):
    """
    Returns the likely root of the word
    :param word: Word
    :param words: Bigger corpus to cross-check with
    :param suffixes: Set of suffixes
    :param lang: Language of the words
    :return: Likely root of the word
    """
    to_stem = True
    while to_stem:
        to_stem = False
        for suffix in suffixes:
            # Transforming ill-shaped forms
            ## Confonant-final forms
            try:
                if word[-1] in lang.consonants:
                    similar_words = [wordform[:len(word)+1] for wordform in words if wordform.startswith(word)
                                     and len(wordform) > len(word) and wordform[len(word)] in
                                     lang.vowels]
                    if similar_words != []:
                        similar_words_dict = dict((form, similar_words.count(form)) for form in set(similar_words))
                        word = max(similar_words_dict, key=similar_words_dict.get)
            except IndexError:
                print("IndexError, word ({}) too short:".format(word))
            # Long-vowel-final forms
            if word[-1] in lang.long_v:
                word = word[:-1] + word[-1].lower()

            # Chopping off a suffix
            if word.endswith(suffix) and word != suffix:
                word = word[:-len(suffix)]
                to_stem = True

    return word

def set_stemmer(words, suffixes, lang):
    """
    Returns a set of likely stems for a set of words.
    returns the first 3 syllables, if yes, then it returns the part without
    the suffix (the root)
    :param words: Set of words to check
    :param suffixes: Suffixes to cross-check words with
    :param lang: Language that words are in
    :return: The set of roots
    """
    wordset = {first_n_syllables(word, 3, ay) for word in words}
    rootset = {wd_stemmer(word, wordset, suffixes, ay) for word in wordset
               if word != ''}

    """
    for suffix in suffixes:
        potential_roots= {word for word in wordset if not word.endswith(suffix)}
        was_suffixed = {word[:-len(suffix)] for word in wordset if word.endswith(suffix)}

        wordset = potential_roots.union(was_suffixed)
        print(len(wordset))
    """

    return rootset


def main():
    roots, suffixes = delucca_reader(
        os.path.join(*[os.pardir, 'Aymara', 'Inputs', 'delucca',
            'ay_delucca_segmented.txt']))
    uti.write_iter(roots, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca.txt']))
    uti.write_iter(suffixes,os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_suffixes_delucca.txt']))

    lowering_table = ay_trans.make_lowering_table()
    roots_trans = ay_trans.transcribe(roots, lowering=lowering_table)
    roots_pl = ay_trans.pl_trans(roots_trans)
    roots_ipa = ay_trans.ipa_trans(roots_trans)
    roots_trans_ej = {ay_trans.nth_transcribe(word, ay.ejectives) for word in roots_trans}
    roots_ej_pl = ay_trans.pl_trans(roots_trans_ej)
    suffixes_trans = ay_trans.transcribe(suffixes, lowering=lowering_table)
    uti.write_iter(roots_trans, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca_preprocessed.txt']))
    uti.write_iter(roots_pl, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca_pl.txt']))
    uti.write_iter(roots_ipa, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca_ipa.txt']))
    uti.write_iter(suffixes_trans, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_suffixes_delucca_preprocessed.txt']))
    uti.write_iter(roots_trans_ej, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca_preprocessed_ejectives.txt']))
    uti.write_iter(roots_ej_pl, os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca_pl_ejectives.txt']))

    ay_words = uti.set_reader(os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_preprocessed.txt']))
    
    subcorpus = rid_of_starters(ay_words, roots_trans)
    roots = set_stemmer(subcorpus, suffixes_trans, ay)

    uti.write_iter(roots, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_roots_from_wordforms_preprocessed.txt']))


if __name__ == '__main__':
    main()

