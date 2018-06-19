#!/usr/bin/python

###################################
# Defining the class of languages #
## Allows for easier reference to #
## natural classes                #
###################################
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
                  'uiUI', 'oeOE', 'aA')
