# create long vowel stem alternants -- identity
# create allomorphs of stems no stem-final vowel (for iri)

# define class of Allomorph
## attributes:
### parse (".allomorph" / "stem_allomorph" / "poly.morphemic.word.form")
### spelling ("spelling")
### type ("root", "suffix", "word form")
### preceding ("v" "no_v" "any")
### final_v (T/F -- or maybe "yes"/"no" ?)
## methods:
### combine(allomorph1, allomorph2)

class Allomorph:
    def __init__(self, parse, spelling, type, preceding, final_v):
        self.parse = parse
        self.spelling = spelling
        self.type = type
        self.preceding = preceding
        self.final_v = final_v
