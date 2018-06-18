#!/usr/bin/python
import os
import itertools
import pandas as pd
from languages import aymara

# Counts observed over expected values
## Defining the Ngram class
class Ngram():
    def __init__(self, name, first, second, frequency):
        self.name = name
        self.first = first
        self.second = second
        self.frequency = frequency

    def O_over_E(self, as_first, as_second, general_gram):
        pass


# Read in the Ngrams
def read_ngrams(path, middle='', capitalize=False):
    """
    Reads in a file as a set of ngrams
    :param path: Where the file is
    :param middle: What character is in the middle
    :param capitalize: If initial of the class should be capitalized
                       default: False
    :return: Set of ngrams
    """
    set_of_ngrams = set()
    with open(path, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            if middle in line.lower() and not line.startswith('stop'):
                bits = line.strip().replace('plain stop', 'plain').split('\t')
                characters = bits[0].split(' ')
                characters = bits[0].split(' ')
                name = ''
                for ch in characters:
                    if ch.lower() == middle:
                        name += 'X'
                    elif capitalize:
                        name += ch[0].upper()
                    else:
                        name += ch[0]
                name = Ngram(name=name, first=name[0], second=name[-1],
                              frequency=int(bits[1]))
                set_of_ngrams.add(name)

    return set_of_ngrams


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
                  if ngram.first == first and ngram.second == second}
    observed = sum({ngram.frequency for ngram in target_set})

    first_set = {ngram for ngram in ngram_set
                 if ngram.first == first}
    second_set = {ngram for ngram in ngram_set
                  if ngram.second == second}
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
    sxs_counts = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'aymara_counts_class_stop_x_stop.txt']),
                              middle='anything', capitalize=True)
    svs_counts = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'aymara_counts_class_stop_x_stop.txt']),
                             middle='vowel', capitalize=True)
    sxs_counts_seg = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'aymara_counts_seg_stop_x_stop.txt']),
                              middle='anything')
    svs_counts_seg = read_ngrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'aymara_counts_seg_stop_v_stop.txt']),
                                 middle='vowel')


    # Counting O/E
    ## Class-level
    oe_sxs_class_df = o_over_e_many_df(sxs_counts, 'AEP')
    oe_sxs_class_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'aymara_oe_sxs_class.csv'
    ]))
    oe_svs_class_df = o_over_e_many_df(svs_counts, 'AEP')
    oe_svs_class_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'aymara_oe_svs_class.csv'
    ]))

    ## Segment-level
    oe_sxs_seg_df = o_over_e_many_df(sxs_counts_seg, aymara.stops)
    oe_sxs_seg_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'aymara_oe_sxs_seg.csv'
    ]))
    oe_svs_seg_df= o_over_e_many_df(svs_counts_seg, aymara.stops)
    oe_svs_seg_df.to_csv(os.path.join(*[
        os.pardir,
        'Outputs',
        'Counts',
        'aymara_oe_svs_seg.csv'
    ]))


if __name__ == '__main__':
    main()