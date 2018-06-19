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
    def __init__(self, plain_stops, asp, ej,
                 fric, affr, nasals, liquids, glides,
                 high_v_short, high_v_long, mid_v_short,
                 mid_v_long, low_v_short, low_v_long):

        self.plain_stops = plain_stops
        self.aspirates = asp
        self.ejectives = ej
        self.stops = plain_stops + asp + ej

        self.fricatives = fric
        self.affricates = affr
        self.obstruents = self.stops + fric + affr

        self.nasals = nasals
        self.liquids = liquids
        self.glides = glides
        self.sonorants = nasals + liquids + glides
        self.consonants = self.obstruents + self.sonorants

        self.high_v = high_v_short + high_v_long
        self.mid_v = mid_v_short + mid_v_long
        self.low_v = low_v_short + low_v_long
        self.vowels = self.high_v + self.mid_v + self.low_v
        self.short_v = high_v_short + mid_v_short + low_v_short
        self.long_v = high_v_long + mid_v_long + low_v_long
        self.nonhigh_v = self.mid_v + self.low_v
        self.nonlow_v = self.high_v + self.mid_v


        self.sounds = self.consonants + self.vowels
        self.non_stops = "".join([sound for sound in self.sounds
                                  if sound not in self.stops])


aymara = Language('ptkcq', 'PTKCQ', 'bdgzG', 'sSxh',
                  '', 'mnN', 'rlY', 'jw',
                  'ui', 'UI', 'oe', 'OE', 'a', 'A')
