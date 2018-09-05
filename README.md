# Transcribed corpus tools
*Python tools for transcribing and extracting quantitative information from phonological word corpora*

## Functions
Scripts are in the ```Scripts/``` folder, and ```Aymara/```, ```Spanish/```, ```English/```, and ```NkoreKiga/``` folders contain input and output files for these languages. Within ```Scripts/```, file names starting with ```tct``` contain utility functions and classes for the entire toolkit, and scripts whose names start with ```ay``` and ```nk``` operate directly with Aymara and Nkore-Kiga corpora, respectively.

```tct_languages.py``` defines a class of ```Language``` as well as variables for the languages used in this project. ```Language``` objects allow for easy reference to natural classes in the given language (e.g. high vowels, stops, and sibilants) in other scripts.

```tct_utility_py``` defines a set of utility functions for opening files and reading their contents into sets, writing iterables into files, writing dictionaries into tab-separated files, as well as for making a transcribed set of words compatible with the space-separated requirements of the UCLA Phonotactic learner (Hayes and Wilson, 2008).

```tct_count_oe.py``` defines a set of functions for counting substrings (```count_many_substr()```), all trigrams (```trigram_counter()```), and for calculating observed-over-expected ratios based on these counts (```o_over_e_many_df()```). ```count_many_substr()``` has options that enable the user to only count word-initial strings, only onsets, as well as to count substrings on a given mapping tier - e.g. to only at the cooccurrence of various kinds of stops within a word, while ignoring all other segments that might intervene.


## Corpora
### Aymara
The set of Aymara words (from an extended version of [An Crúbadán](http://crubadan.org/languages/ay): Scannell, 2007) were cleaned from numbers and non-alphanumeric characters, converted into lower case and 255 words were discarded because they contained a hyphen ("-"). The source file for Aymara (from Marín, 1992) was manually searched for apostrophe-related typos, 2 of them were corrected (_muru'q_ to _muruq'_ and _la'qa_ to _laq'a_) and converted into lowercase. They were then cross-checked with a set of the Spanish and English words. The sources for the Spanish and English words were the [CORLEC Corpus](http://www.lllf.uam.es/ESP/Corlec.html) (Marín, 1992), and the [CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict) (Weide, 2005), respectively. Matches were separated from the rest of the dataset, because they are presumably loan words. The filtered set of Aymara words with no Spanish or English loans in it contains 81,325 unique word forms (```Aymara/Outputs/Aymara_words_no_sp_en.txt```), the presumable Spanish loans were 188 words (```Aymara/Outputs/Spanish_loans.txt```), and the set of putative English loans totalled at 128 words (```Outputs/English_loans.txt```) - the latter two sets might overlap.  

An additional 11 words were discarded at this stage because of misplaced "'" characters - indicating ejectives. 1 because of missing vowel (_j'cha_), 3 because of ejectival closure between vowels (_cha'amañchistañapatakiwa_, _chu'uqi_, _chi'är_), 3 word forms had stops with both aspiration and ejectival closure (_kh'antatina_, _ph'ich'i_, _wichh'inqhapa_), and 4 word forms had ejectival closure marked in places where the only only adjacent consonant was not a stop (_huka'mp_, _arts'i_, _his'a_, _inamayayt'a'yi_). Words containing more than 2 adjacent instances of the same sound (e.g. 'aaa') were also removed. This resulted in a *set of 81,206 words* (containing mono- and polymorphemic Aymara word forms).

The ```Script/ay_transcriber.py``` transcribed the Aymara word list according to three transcription systems: the international Phonetic Alphabet (IPA, ```Outputs/Transcription/aymara_ipa.txt```), an intermediary system, in which each sound is in a one-to-one correspondance representing it (```Outputs/Transcription/aymara_preprocessed.txt```, key: ```Aymara/aymara_trans_key.txt```), and a system compatible with the UCLA Phonotactic Learner with the same key (```Outputs/Transcription/aymara_pl.txt```).


#### Additional operations
```Scripts/ay_delucca_rooter.py``` reads in a set of previously segmented word forms from the de Lucca dictionary (1987) and splits them into roots and suffixes. It then uses this list of suffixes and stems to eliminate non-root forms from the wordlist in the ```Outputs/Transcription/aymara_preprocessed.txt``` file. Words are eliminated if they start with a root from the de Lucca dictionary. Moreover, since roots in Aymara are typically 1-3 syllables long and there are no prefixes in the languages, words are reduced to their first 3 syllables. These 3-syllable substrings are then checked for word-final suffixes.

```Scripts/ay_counter.py``` contains various functions for counting relevant ngrams in the ```Outputs/Transcription/aymara_preprocessed.txt``` file for word forms and ```Inputs/delucca/ay_trans_roots_delucca.txt``` for roots. It can count instances of one ngram, multiple ones, with the options of only looking for word-initial matches and projecting on a certain tier. It outputs results into the ```Outputs/Counts/Raw/``` and ```Outputs/Counts/Lists/``` folders (for counts and list of matching words, respectively. (This file might be separated into a language-specific file - with a ```main()``` function only - and a general file that can be used in other corpora.)

```Scripts/ay_obs_over_exp.py``` counts observed-over-expected values on the outputs of ```ay_counter.py``` in ```Outputs/Counts/Raw/``` for both word forms and roots.


### Nkore-Kiga
The Nkore-Kiga corpus is a version of a dictionary by Taylor (1959), digitized as part of the Comparative Bantu On-Line Dictionary Project ([CBOLD](http://www.linguistics.berkeley.edu/~jblowe/CBOLD/)). The digitized original contains 12,574 words in total. After cross-referencing it with the original dictionary, 56 spelling mistakes were manually corrected. After words containing non-letter characters were filtered out, 11,400 word forms and 6,520 root forms were collected. In addition, a list of 11,404 word forms was compiled, where the root is separated from the prefixes by a '+' character (```Scripts/nk_reader_parser.py```).

These lists were each transcribed into IPA, and according to a one-to-one sound-to-letter key (```NkoreKigankorekiga_transcription_key.txt```), which was also made UCLA Phonotactic Learner-compatible (```Scripts/nk_transcriber.py```). These files can be found in ```NkoreKiga/Outputs/Transcription/```.

```Scripts/nk_counter.py``` and ```Scripts/nk_obs_over_exp.py``` count some samples of substrings in the corpora, and calculate observed-over-expected values based on them. The outputs of these programs can be found in ```NkoreKiga/Outputs/Counts/```.


## References
Hayes, Bruce and Wilson, Colin. 2008. A maximum entropy model of phonotactics and phonotactic learning. _Linguistic inquiry_, 39(3), pp.379-440.

de Lucca, Manuel. 1987. _Diccionario practico aymara-castellano castellano-aymara_. Cochabamba:Los Amigos del Libro.

Marín, Marcos F. 1992. El Corpus Oral de Referencia de la Lengua Española contemporánea Project Report. Universidad Autónoma de Madrid. Available at <http://www.lllf.uam.es/ESP/Corlec.html> 

Scannell, Kevin P. 2007. The Crúbadán Project: Corpus building for under-resourced languages. _Building and Exploring Web Corpora: Proceedings of the 3rd Web as Corpus Workshop_. Vol. 4: pp.5-15.

Taylor, C., 1959. A simplified Runyankore-Rukiga-English and English-Runyankore-Rukiga dictionary: in the 1955 revised orthography with tone-markings and full entries under prefixes. Eagle Press.

Weide, Robert. _The Carnegie mellon pronouncing dictionary (cmudict. 0.6)_. Available at:  <http://www.speech.cs.cmu.edu/cgi-bin/cmudict> 2005.

