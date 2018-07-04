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

        self.plain_stops = tuple(plain_stops)
        self.aspirates = tuple(asp)
        self.ejectives = tuple(ej)
        self.stops = tuple(plain_stops + asp + ej)

        self.fricatives = tuple(fric)
        self.affricates = tuple(affr)
        self.obstruents = self.stops + tuple(fric + affr)


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
        self.non_stops = [sound for sound in self.sounds
                          if sound not in self.stops]


aymara = Language('ptkcq', 'PTKCQ', 'bdgzG', 'sSxh',
                  '', 'mnN', 'rlY', 'jw',
                  'ui', 'UI', 'oe', 'OE', 'a', 'A')
