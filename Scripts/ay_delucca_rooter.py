import ay_sp_en_filter as ay_filter
import ay_transcriber as ay_trans
from languages import aymara
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
            if counter == 3 and (word[i+1] in lang.vowels or
                (word[i+1] in lang.stops and word[i+2] in lang.vowels)):
                return syllables
        except IndexError:
            return word
    return word



def stemmer(words, suffixes, lang):
    """
    Returns a set of likely stems for a set of words.
    returns the first 3 syllables, if yes, then it returns the part without
    the suffix (the root)
    :param words: Set of words to check
    :param suffixes: Suffixes to cross-check words with
    :param lang: Language that words are in
    :return: The set of roots
    """
    wordset={first_n_syllables(word, 3, aymara) for word in words}

    for suffix in suffixes:
        potential_roots= {word for word in wordset if not word.endswith(suffix)}
        was_suffixed = {word[:-len(suffix)] for word in wordset if word.endswith(suffix)}

        wordset = potential_roots.union(was_suffixed)
        print(len(wordset))

    return wordset


def main():
    roots, suffixes = delucca_reader(
        os.path.join(*[os.pardir, 'Inputs', 'delucca', 'ay_delucca_segmented.txt']))
    ay_filter.write_iter(roots, os.path.join(*[
        os.pardir, 'Inputs', 'delucca', 'ay_roots_delucca.txt']))
    ay_filter.write_iter(suffixes,os.path.join(*[
        os.pardir, 'Inputs', 'delucca', 'ay_suffixes_delucca.txt']))

    lowering_table = ay_trans.make_lowering_table()
    roots_trans = ay_trans.transcribe(roots, lowering=lowering_table)
    suffixes_trans = ay_trans.transcribe(suffixes, lowering=lowering_table)
    ay_filter.write_iter(roots_trans, os.path.join(*[
        os.pardir, 'Inputs', 'delucca', 'ay_trans_roots_delucca.txt']))
    ay_filter.write_iter(suffixes_trans, os.path.join(*[
        os.pardir, 'Inputs', 'delucca', 'ay_trans_suffixes_delucca.txt']))

    ay_words = ay_trans.set_reader(os.path.join(*[os.pardir,
                                                  'Outputs',
                                                  'Transcription',
                                                  'aymara_preprocessed.txt']))
    subcorpus = rid_of_starters(ay_words, roots_trans)
    roots = stemmer(subcorpus, suffixes_trans, aymara)

    ay_filter.write_iter(roots, os.path.join(*[
        os.pardir, 'Outputs', 'aymara_roots_trans.txt']))

if __name__ == '__main__':
    main()

