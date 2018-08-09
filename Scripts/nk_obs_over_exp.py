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
import tct_count_oe_func as cou
from tct_languages import nkore_kiga as nk
import os


# Read in trigram counts
nk_trigram_counts_f = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_tri_forms.txt')))
nk_trigram_counts_r = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_tri_roots.txt')))
nk_trigram_counts_p = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_tri_formssep.txt')))
nk_trigram_counts = [nk_trigram_counts_f, nk_trigram_counts_r,
                      nk_trigram_counts_p]

# Read in sibilant tier counts
sib_counts_seg_f = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_sib_tier_forms.txt')), middle='anything')
sib_counts_seg_r = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_sib_tier_roots.txt')), middle='anything')
sib_counts_seg_p = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_sib_tier_formssep.txt')), middle='anything')
nk_sib_tier_counts = [sib_counts_seg_f, sib_counts_seg_r,
                      sib_counts_seg_p]

# Read in sibilant fricative tier counts
sib_fric_counts_seg_f = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_sib_fric_tier_forms.txt')), middle='anything')
sib_fric_counts_seg_r = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_sib_fric_tier_roots.txt')), middle='anything')
sib_fric_counts_seg_p = cou.read_ngrams(os.path.join(*(
    os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'Raw',
    'nk_counts_sib_fric_tier_formssep.txt')), middle='anything')
nk_sib_fric_tier_counts = [sib_fric_counts_seg_f, sib_fric_counts_seg_r,
                      sib_fric_counts_seg_p]

nk_count_names = ['forms', 'roots', 'formssep']

for i, c_name in enumerate(nk_count_names):
    # Trigram O/Es
    tri_count = nk_trigram_counts[i]
    oe_trigram_class_df = \
        cou.o_over_e_many_df(tri_count,
                             [str(nk.sibilants_anterior),
                              str(nk.sibilants_postanterior)])
    oe_trigram_class_df.to_csv(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'OE',
        'nk_oe_trigram_class_{}.csv'.format(c_name))))

    oe_trigram_seg_df = cou.o_over_e_many_df(tri_count, nk.sibilants)
    oe_trigram_seg_df.to_csv(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'OE',
        'nk_oe_trigram_seg_{}.csv'.format(c_name))))


    # Sibilant tier O/Es
    sib_count = nk_sib_tier_counts[i]
    oe_sib_class_df = \
        cou.o_over_e_many_df(sib_count,
                             [str(nk.sibilants_anterior),
                              str(nk.sibilants_postanterior)])
    oe_sib_class_df.to_csv(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'OE',
        'nk_oe_sib_tier_class_{}.csv'.format(c_name))))

    oe_sib_seg_df = cou.o_over_e_many_df(sib_count, nk.sibilants)
    oe_sib_seg_df.to_csv(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'OE',
        'nk_oe_sib_tier_seg_{}.csv'.format(c_name))))


    # Sibilant fricative tier O/Es
    sib_fric_count = nk_sib_fric_tier_counts[i]
    oe_sib_fric_class_df = \
        cou.o_over_e_many_df(sib_fric_count,
                             [str(nk.sibilant_fricatives_ant),
                              str(nk.sibilant_fricatives_post)])
    oe_sib_fric_class_df.to_csv(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'OE',
        'nk_oe_sib_fric_tier_class_{}.csv'.format(c_name))))

    oe_sib_fric_seg_df = cou.o_over_e_many_df(sib_fric_count,
                                         nk.sibilant_fricatives)
    oe_sib_fric_seg_df.to_csv(os.path.join(*(
        os.pardir, 'NkoreKiga', 'Outputs', 'Counts', 'OE',
        'nk_oe_sib_fric_tier_seg_{}.csv'.format(c_name))))
