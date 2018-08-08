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

###################################
# Defining the class of languages #
## Allows for easier reference to #
## natural classes                #
###################################

# Further attributes might be added to the class in the future depending on what languages will be implemented.
class Language:
    def __init__(self, plain_stops, sib_plain, asp, sib_asp, ej, sib_ej,
                 fric, sib_fric, affr, sib_affr, nasals, liquids, glides,
                 high_v_short, high_v_long, mid_v_short,
                 mid_v_long, low_v_short, low_v_long):

        self.plain_stops = tuple(plain_stops + sib_plain)
        self.aspirates = tuple(asp + sib_asp)
        self.ejectives = tuple(ej + sib_ej)
        self.stops = self.plain_stops + self.aspirates + \
                     self.ejectives
        self.sibilant_stops = tuple(sib_plain + sib_asp + sib_ej)
        self.nonsib_stops = tuple(plain_stops + asp + ej)

        self.fricatives = tuple(fric + sib_fric)
        self.sibilant_fricatives = tuple(sib_fric)
        self.affricates = tuple(affr + sib_affr)
        self.sibilant_affricates = tuple(sib_affr)
        self.obstruents = self.stops + tuple(fric + affr)
        self.sibilants = self.sibilant_stops + \
                         tuple(sib_fric + sib_affr)
        self.nonsib_obstruents = tuple(plain_stops + asp +
                                       ej + fric + affr)

        self.nasals = tuple(nasals)
        self.liquids = tuple(liquids)
        self.glides = tuple(glides)
        self.sonorants = tuple(nasals + liquids + glides)
        self.consonants = self.obstruents + self.sonorants

        self.high_v = tuple(high_v_short + high_v_long)
        self.mid_v = tuple(mid_v_short + mid_v_long)
        self.low_v = tuple(low_v_short + low_v_long)
        self.vowels = self.high_v + self.mid_v + self.low_v
        self.short_v = tuple(high_v_short + mid_v_short + low_v_short)
        self.long_v = tuple(high_v_long + mid_v_long + low_v_long)
        self.nonhigh_v = self.mid_v + self.low_v
        self.nonlow_v = self.high_v + self.mid_v


        self.sounds = self.consonants + self.vowels
        self.non_stops = tuple([sound for sound in self.sounds
                          if sound not in self.stops])
        self.nonsibilants = tuple([sound for sound in self.sounds
                          if sound not in self.sibilants])


aymara = Language('ptkq', 'c', 'PTKQ', 'C', 'bdgG', 'z', 'sS', 'xh',
                  '', '', 'mnN', 'rlY', 'jw',
                  'ui', 'UI', 'oe', 'OE', 'a', 'A')

nkore_kiga = Language('ptk', 'T', '', '', 'bdg', 'D', 'fvh', 'sSzZ',
                      '', '', 'mnNY', 'r', 'jw',
                      'ui', 'UI', 'oe', 'OE', 'a', 'A')
