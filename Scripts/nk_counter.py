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
import tct_count_oe as cou
from tct_languages import nkore_kiga as nk
import os

# This file might be later separated into a language-specific file
# (with a ```main()``` function only)
# and a general file that can be used in other corpora.


def main():
    sib_sib = {sib1 + sib2 for sib1 in nk.sibilants for sib2 in nk.sibilants}

    nk_roots = {word.replace(' ', '') for word in uti.set_reader(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription', 'Preprocessed',
        'nk_roots_preprocessed.txt')))}
    nk_forms = {word.replace(' ', '') for word in uti.set_reader(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription', 'Preprocessed',
        'nk_forms_preprocessed.txt')))}
    nk_forms_parsed = {word.replace(' ', '') for word in uti.set_reader(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Transcription', 'Preprocessed',
        'nk_forms_sep_preprocessed.txt')))}

    nk_corpora = [nk_roots, nk_forms, nk_forms_parsed]
    corp_names = ['roots', 'forms', 'formssep']

    for i, corpus in enumerate(nk_corpora):
        corp_name = corp_names[i]

        # All trigrams
        trigram_counts = cou.trigram_counter(corpus)
        uti.write_dict(trigram_counts, os.path.join(*(
            os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
            'nk_counts_tri_{}.txt'.format(corp_name))))

        # Sibilant tier
        nk_ss_list, nk_ss_count = cou.count_many_substr(
            sib_sib, corpus, nk, tier=nk.sibilants, return_set=True)
        nk_ss_count_formatted = {key[0] + ' anything ' + key[1]:
                                     nk_ss_count[key]
                                    for key in nk_ss_count.keys()}
        uti.write_dict(nk_ss_count_formatted, os.path.join(*(
            os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
            'nk_counts_sib_tier_{}.txt'.format(corp_name))))

        nk_ss_fric_list, nk_ss_fric_count = cou.count_many_substr(
            sib_sib, corpus, nk, tier=nk.sibilant_fricatives,
            return_set=True)
        nk_ss_fric_count_formatted = {key[0] + ' anything ' + key[1]:
                                     nk_ss_fric_count[key]
                                 for key in nk_ss_fric_count.keys()}
        uti.write_dict(nk_ss_fric_count_formatted, os.path.join(*(
            os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
            'nk_counts_sib_fric_tier_{}.txt'.format(corp_name))))




if __name__ == '__main__':
    main()
