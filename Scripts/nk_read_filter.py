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
import csv
import string
from languages import nkore_kiga as nkore_kiga
import ay_sp_en_filter as filt

def read_roots_forms(file, lang, sep="\t", re_roots=True, re_forms=True, re_forms_sep=True):
    """
    Reads in file, returns set of roots, set of word forms, or both.
    :param file: File to read in
    :param sep: Separator (delimiter) in the file
    :param lang: Natural language of words in the corpus
    :param re_roots: Whether it should return roots
                     default: True
    :param re_forms: Whether it should return forms
                     default: True
    :param re_forms_sep: Whether it should return a set of forms in which prefixes and root
                         are separated by a '+'
                         default: true
    :return: A set of roots, a set of words forms or both
    """
    roots = set()
    forms = set()
    forms_sep = set()
    to_return = []


    to_keep_ch = {"'", "+"}
    to_remove_ch = set(string.punctuation) - to_keep_ch - {'-'}
    table_keep = {ord(char): None for char in to_keep_ch}
    table_remove = {ord(char): None for char in to_remove_ch}

    to_strip_pre_ch = {'?', '*', '.'}
    table_pre = {ord(char): None for char in to_strip_pre_ch}

    with open(file, encoding='utf-8') as f:
        csv_f = csv.reader(f, delimiter=sep)
        next(csv_f, None)

        for record in csv_f:
            form = record[0].translate(table_pre)
            prefix = record[1].translate(table_pre).replace(' ', '')
            root = record[2].translate(table_pre)
            if form != '' and form[-1] != 's' and form[-1] != 'n':
                root_bound = root.rstrip('sn')
            else:
                root_bound = root
            if len(set(root.lower())) < 2 or len({sound for sound in root.lower()
                                                   if sound in lang.vowels}) == 0:
                continue

            if (prefix + root_bound).lower() == form.lower():
                form_sep = prefix + '+' + root_bound
            elif form.lower().startswith((prefix + '+' + root_bound).lower()):
                form_sep = prefix + '+' + root_bound + '+' + form.partition(prefix + root_bound)[3]
            elif prefix == '' and root_bound == '':
                form_sep = form
            elif prefix == '' or root_bound == '':
                continue


            if re_roots:
                clean_word(root, table_remove, table_keep, roots)
                if root == '' and form != '':
                    clean_word(form, table_remove, table_keep, roots)
            if re_forms:
                clean_word(form, table_remove, table_keep, forms)
            if re_forms_sep and form_sep != '':
                clean_word(form_sep, table_remove, table_keep, forms_sep)
                if form_sep == '+' and form != '':
                    clean_word(form, table_remove, table_keep, forms_sep)

        if re_roots:
            to_return.append(roots)
        if re_forms:
            to_return.append(forms)
        if re_forms_sep:
            to_return.append(forms_sep)

        return to_return


def clean_word(wrd, table_rm, table_kp, st):
    """
    Makes a word form lowercase, strips from certain characters, and if the result
    is only letters, it adds it to a set
    :param wrd: Word to clean
    :param table_rm: Set of characters to remove from it
    :param table_kp: Set of non-letters to keep in words
    :param st: Set to add word to if it only has letters
    :return: None, adds to set
    """
    wrd = wrd.translate(table_rm)
    wrd = wrd.lower()
    if wrd.translate(table_kp).isalpha() and wrd not in st and wrd != '':
        st.add(wrd)


def main():
    # Read in file
    [roots, forms, forms_sep] = read_roots_forms(os.path.join(*[
        os.pardir, 'NkoreKiga', 'KigaNkore_Taylor1959.txt']), nkore_kiga)

    """
    # Diagnostics
    # print(len(roots))
    # print(len(forms))
    # print(len(forms_sep))

    # print({form_sep for form_sep in forms_sep if form_sep.replace('+', '') not in forms})
    # st = {form_sep.replace('+', '') for form_sep in forms_sep}
    # print({form for form in forms if form not in st})
    """

    # Write out roots
    filt.write_iter(roots, os.path.join(*[
        os.pardir, 'NkoreKiga', 'Outputs',
        'nk_roots_pretrans.txt']))

    # Write out wordforms
    filt.write_iter(forms, os.path.join(*[
        os.pardir, 'NkoreKiga', 'Outputs',
        'nk_forms_pretrans.txt']))

    # Write out parsed wordforms
    filt.write_iter(forms_sep, os.path.join(*[
        os.pardir, 'NkoreKiga', 'Outputs',
        'nk_forms_sep_pretrans.txt']))


if __name__ == '__main__':
    main()


