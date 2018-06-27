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
    :param subcase: If there are multiple options in the source document,
                    which subcase it should regard
    :param length: Length of the Ngram
    :return: Set of ngram:
    """
    set_of_ngrams = set()
    with open(path, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            if middle in line.lower() and not line.startswith('stop'):
                bits = line.strip().replace('plain stop', 'plain').\
                    replace(subcase, '_'+subcase.strip()).split('\t')
                name = bits[0].split(' ')
                if subcase == '' and len(name) > length:
                    continue
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
    :param first: First segment of the ngram
    :param second: Second segment of the ngram
    :return: The O/E ratio
    """
    total_count = sum({ngram.frequency for ngram in ngram_set})

    target_set = {ngram for ngram in ngram_set
                  if ngram.first == first and ngram.last == second}
    observed = sum({ngram.frequency for ngram in target_set})

    first_set = {ngram for ngram in ngram_set
                 if ngram.first == first}
    second_set = {ngram for ngram in ngram_set
                  if ngram.last == second}
    first_prob = sum({ngram.frequency for ngram in first_set}) / total_count
    second_prob = sum({ngram.frequency for ngram in second_set}) / total_count


    expected = first_prob * second_prob * total_count
    try:
        o_e = observed / expected
    except ZeroDivisionError:
        o_e = 'Expected is 0.'
        print('First prob = {}\n'
              'Second prob = {}\n'
              'Total count = {}'.format(str(first_prob),
                                         str(second_prob),
                                         str(total_count)))
        print(first, second)
    return observed, expected, o_e


# Function that returns a DataFrame of O/E values for a set of Ngrams
def o_over_e_many_df(counts, segments):
    """
    Transforms raw counts into a pandas data frame containing observed,
    expected, and O/E values
    :param counts: ngram object containing counts
    :param segments: names of columns -- classes of segments to look at
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
    ## Any match
    sxs_counts = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs.txt']),
                              middle='anything')
    svs_counts = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_all_sxs_svs.txt']),
                             middle='vowel')
    sxs_counts_seg = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_all_sxs.txt']),
                              middle='anything')
    svs_counts_seg = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_all_svs.txt']),
                                 middle='vowel')

    ## Word-initial matches
    sxs_counts_init = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs.txt']),
                             middle='anything')
    svs_counts_init = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_class_initial_sxs_svs.txt']),
                             middle='vowel')
    sxs_counts_seg_init = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_initial_sxs.txt']),
                                 middle='anything')
    svs_counts_seg_init = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'Raw', 'aymara_counts_seg_initial_svs.txt']),
                                 middle='vowel')

    # Counting O/E
    ## Class-level
    ### All matches
    oe_sxs_class_df = o_over_e_many_df(sxs_counts,
                                       ['aspirate', 'ejective', 'plain'])
    oe_sxs_class_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_class_all.csv'
    ]))
    oe_svs_class_df = o_over_e_many_df(svs_counts,
                                       ['aspirate', 'ejective', 'plain'])
    oe_svs_class_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_class_all.csv'
    ]))

    ### Word-initial matches
    oe_sxs_class_init_df = o_over_e_many_df(sxs_counts_init,
                                       ['aspirate', 'ejective', 'plain'])
    oe_sxs_class_init_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_class_init.csv'
    ]))
    oe_svs_class_init_df = o_over_e_many_df(svs_counts_init,
                                       ['aspirate', 'ejective', 'plain'])
    oe_svs_class_init_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_class_init.csv'
    ]))

    ## Segment-level
    ### All matches
    oe_sxs_seg_df = o_over_e_many_df(sxs_counts_seg, ay.stops)
    oe_sxs_seg_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_seg_all.csv'
    ]))
    oe_svs_seg_df= o_over_e_many_df(svs_counts_seg, ay.stops)
    oe_svs_seg_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_seg_all.csv'
    ]))

    ### Word-initial matches
    oe_sxs_seg_init_df = o_over_e_many_df(sxs_counts_seg_init, ay.stops)
    oe_sxs_seg_init_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_sxs_seg_initial.csv'
    ]))
    oe_svs_seg_init_df = o_over_e_many_df(svs_counts_seg_init, ay.stops)
    oe_svs_seg_init_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'OE',
        'aymara_oe_svs_seg_initial.csv'
    ]))


if __name__ == '__main__':
    main()