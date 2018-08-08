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
##################################################
# Defines utility functions for handling corpora #
##################################################

# Reading newline-separated file into set
def set_reader(path):
    """
    Reads in file into a set.
    :param path: location of text file with one word/line
    :return: a set of words
    """
    with open(path, "r", encoding="utf-8") as f:
        lst = {line.strip() for line in f}

    return lst


# Writing an iterable into a file
def write_iter(iter, path):
    """
    Writes list of words to file.
    :param iter: iterable to be written to file
    :param path: path of new file
    :return: None
    """
    lst = list(iter)
    lst.sort()
    with open(path, 'w', encoding='utf-8') as output_w:
        for item in lst:
            output_w.write(item + '\n')


# Writing a dictionary into a tab-separated file
def write_dict(dict, path):
    """
    Writes dictionary into text file
    :param dict: dictionary to be written into file
    :param path: path of file to be written to
    :return: None
    """
    with open(path, 'w', encoding='utf-8') as output_w:
        for key in sorted(dict):
            output_w.write('{}\t{}\n'.format(key, int(dict[key])))


# Transcribes set of pre-processed words into UCLA PL compatible ones
def pl_trans(st):
    """
    Transcribes a set of words in the style of the UCLA Phonotactic Learner
    :param st: input set of preprocessed words
    :return: pl_set a set of UCLA PL-compatible words
    """
    pl_set = {" ".join(list(wrd)) for wrd in st}

    return pl_set