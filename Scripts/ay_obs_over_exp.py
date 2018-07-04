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
import itertools
import pandas as pd
from languages import aymara as ay

# This file might be later separated into a language-specific file
# (with a ```main()``` function only)
# and a general file that can be used in other corpora.


##################################################################
# Counts observed over expected values of (non-adjacent) bigrams #
##################################################################
# The Ngram class
class Ngram():
    def __init__(self, name, first, second, last, frequency):
        self.name = name
        self.first = first
        self.second = second
        self.last = last
        self.frequency = frequency


# Function for reading in the Ngrams
def read_ngrams(path, middle='', subcase='', length=3):
    """
    Reads in a file as a set of ngrams
    :param path: Where the file is
    :param middle: What character is in the middle
                   default: empty string
    :param subcase: If there are multiple options in the source document,
                    which subcase it should regard
                    default: empty string
    :param length: Length of the Ngram
                   default: 3
    :return: Set of ngram:
    """
    set_of_ngrams = set()
    subcase_suffix = '_' + subcase.strip()
    with open(path, 'r', encoding='utf-8') as in_f:
        for i, line in enumerate(in_f):
            if middle in line.lower() and not line.startswith('stop'):
                bits = line.strip().replace('plain stop', 'plain').split('\t')
                if subcase != '':
                    bits[0] = bits[0].replace(subcase, subcase_suffix)
                if ' ' in bits[0]:
                    name = bits[0].split(' ')
                else:
                    name = list(bits[0])
                if len(name) > length:
                    continue
                if middle != '':
                    name[name.index(middle)] = 'X'

                name = Ngram(name=name, first=name[0], second=name[1],
                             last=name[-1], frequency=int(bits[1]))

                set_of_ngrams.add(name)

    return set_of_ngrams


# Function for counting O/E
def o_over_e(ngram_set, first, second):
    """
    Counts an observed-over-expected (O/E) ratio.
    :param ngram_set: Set of ngrams with their counts
    :param first: First segment of the ngram as a list
    :param second: Second segment of the ngram as a list
    :return: The O/E ratio
    """
    total_count = sum({ngram.frequency for ngram in ngram_set})

    target_set = {ngram for ngram in ngram_set
                  if ngram.first in first and ngram.last in second}
    observed = sum({ngram.frequency for ngram in target_set})

    first_set = {ngram for ngram in ngram_set
                 if ngram.first in first}
    second_set = {ngram for ngram in ngram_set
                  if ngram.last in second}

    try:
        first_prob = sum({ngram.frequency for ngram in first_set}) / total_count
        second_prob = sum({ngram.frequency for ngram in second_set}) / total_count
    except ZeroDivisionError:
        return 'Total count is 0.'

    expected = first_prob * second_prob * total_count
    try:
        o_e = observed / expected
    except ZeroDivisionError:
        print('Expected is 0.')
        print('First prob = {}; Second prob = {}'
              .format(str(first_prob), str(second_prob)))
        print(first, second)
        return None
    return observed, expected, o_e


# Function that returns a DataFrame of O/E values for a set of Ngrams
def o_over_e_many_df(counts, segments):
    """
    Transforms raw counts into a pandas data frame containing observed,
    expected, and O/E values
    :param counts: ngram object containing counts
    :param segments: names of rows and columns
                    (i.e. classes of segments to look at)
    :return:
    """
    combinations = itertools.product(segments, segments)
    oe_dict = {}
    for (first, second) in combinations:
        o, e, oe = o_over_e(counts, first, second)
        if first not in oe_dict:
            oe_dict[first] = {}
        oe_dict[first][second] = \
            "{:.1f}/{:.2f} = {:.4f}".format(o, e, oe)

    oe_df = pd.DataFrame.from_dict(oe_dict, orient='index')
    return oe_df



def main():
    # Reading in the files
    ## Words
    ### All matches
    sxs_counts_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_words.txt']),
                              middle='anything')
    svs_counts_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_words.txt']),
                             middle='vowel')
    """
    sxs_counts_w_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_words.txt']),
                             middle='anything', subcase=' (heterorganic)')
    svs_counts_w_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_words.txt']),
                             middle='vowel', subcase=' (heterorganic)')
    """
    sxs_counts_seg_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_all_sxs_words.txt']),
                              middle='anything')
    svs_counts_seg_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_all_svs_words.txt']),
                                 middle='vowel')

    ### Word-initial matches
    sxs_counts_init_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_words.txt']),
                             middle='anything')
    svs_counts_init_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_words.txt']),
                             middle='vowel')
    """
    sxs_counts_init_w_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_words.txt']),
                                    middle='anything', subcase=' (heterorganic)')
    svs_counts_init_w_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_words.txt']),
                                    middle='vowel', subcase=' (heterorganic)')
    """
    sxs_counts_seg_init_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_initial_sxs_words.txt']),
                                 middle='anything')
    svs_counts_seg_init_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_initial_svs_words.txt']),
                                 middle='vowel')


    ## Roots
    ### All matches
    sxs_counts_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_roots.txt']),
                               middle='anything')
    svs_counts_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_roots.txt']),
                               middle='vowel')
    """
    sxs_counts_r_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_roots.txt']),
                                   middle='anything', subcase=' (heterorganic)')
    svs_counts_r_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs_roots.txt']),
                                   middle='vowel', subcase=' (heterorganic)')
    """
    sxs_counts_seg_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_all_sxs_roots.txt']),
                                   middle='anything')
    svs_counts_seg_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_all_svs_roots.txt']),
                                   middle='vowel')

    ### Word-initial matches
    sxs_counts_init_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_roots.txt']),
                                    middle='anything')
    svs_counts_init_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_roots.txt']),
                                    middle='vowel')
    """
    sxs_counts_init_r_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_roots.txt']),
                                        middle='anything', subcase=' (heterorganic)')
    svs_counts_init_r_het = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs_roots.txt']),
                                        middle='vowel', subcase=' (heterorganic)')
    """
    sxs_counts_seg_init_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_initial_sxs_roots.txt']),
                                        middle='anything')
    svs_counts_seg_init_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_initial_svs_roots.txt']),
                                        middle='vowel')

    ### Trigrams
    trigram_counts_seg_w = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw',
        'aymara_counts_seg_all_trigrams_words.txt']))
    trigram_counts_seg_r = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw',
        'aymara_counts_seg_all_trigrams_roots.txt']))


    # Counting O/E
    ## Words
    ### All matches
    oe_sxs_class_w_df = \
        o_over_e_many_df(sxs_counts_w,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_sxs_class_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_class_all_words.csv'
    ]))
    oe_svs_class_w_df = \
        o_over_e_many_df(svs_counts_w,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_svs_class_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_class_all_words.csv'
    ]))

    oe_sxs_seg_w_df = o_over_e_many_df(sxs_counts_seg_w, ay.stops)
    oe_sxs_seg_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_seg_all_words.csv'
    ]))
    oe_svs_seg_w_df = o_over_e_many_df(svs_counts_seg_w, ay.stops)
    oe_svs_seg_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_seg_all_words.csv'
    ]))

    oe_trigram_seg_w_df = o_over_e_many_df(trigram_counts_seg_w, ay.stops)
    oe_trigram_seg_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_trigram_seg_all_words.csv'
    ]))


    ### Word-initial matches
    oe_sxs_class_init_w_df = \
        o_over_e_many_df(sxs_counts_init_w,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_sxs_class_init_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_class_init_words.csv'
    ]))
    oe_svs_class_init_w_df = \
        o_over_e_many_df(svs_counts_init_w,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_svs_class_init_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_class_init_words.csv'
    ]))

    oe_sxs_seg_init_w_df = o_over_e_many_df(sxs_counts_seg_init_w, ay.stops)
    oe_sxs_seg_init_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_seg_initial_words.csv'
    ]))
    oe_svs_seg_init_w_df = o_over_e_many_df(svs_counts_seg_init_w, ay.stops)
    oe_svs_seg_init_w_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_seg_initial_words.csv'
    ]))


    ## Roots
    ### All matches
    oe_sxs_class_r_df = \
        o_over_e_many_df(sxs_counts_r,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_sxs_class_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_class_all_roots.csv'
    ]))
    oe_svs_class_r_df = \
        o_over_e_many_df(svs_counts_r,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_svs_class_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_class_all_roots.csv'
    ]))

    oe_sxs_seg_r_df = o_over_e_many_df(sxs_counts_seg_r, ay.stops)
    oe_sxs_seg_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_seg_all_roots.csv'
    ]))
    oe_svs_seg_r_df = o_over_e_many_df(svs_counts_seg_r, ay.stops)
    oe_svs_seg_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_seg_all_roots.csv'
    ]))

    ### Word-initial matches
    oe_sxs_class_init_r_df = \
        o_over_e_many_df(sxs_counts_init_r,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_sxs_class_init_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_class_init_roots.csv'
    ]))
    oe_svs_class_init_r_df = \
        o_over_e_many_df(svs_counts_init_r,
                         [('aspirate',), ('ejective',), ('plain',)])
    oe_svs_class_init_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_class_init_roots.csv'
    ]))

    oe_sxs_seg_init_r_df = o_over_e_many_df(sxs_counts_seg_init_r, ay.stops)
    oe_sxs_seg_init_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_seg_initial_roots.csv'
    ]))
    oe_svs_seg_init_r_df = o_over_e_many_df(svs_counts_seg_init_r, ay.stops)
    oe_svs_seg_init_r_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_seg_initial_roots.csv'
    ]))




if __name__ == '__main__':
    main()