# Transcribed corpus tools
## Python tools for transcribing and extracting quantitative information from phonological word corpora

### Functions
Scripts are in the ```Scripts/``` folder, and ```Aymara/```, ```Spanish/```, ```English/```, and ```NkoreKiga/``` folders contain input and output files for these languages. Within ```Scripts/```, file names starting with ```tct``` contain utility functions and classes for the entire toolkit, and scripts whose names start with ```ay``` and ```nk``` operate directly with Aymara and Nkore-Kiga corpora, respectively.

```tct_languages.py``` defines a class of Language as well as variables for the languages used in this project. Language objects allow for easy reference to natural classes in the given language (e.g. high vowels, stops, and sibilants) in other scripts.

```tct_utility_py``` defines a set of utility functions for opening files and reading their contents into sets, writing iterables into files, writing dictionaries into tab-separated files, as well as for making a transcribed set of words compatible with the space-separated requirements of the UCLA Phonotactic learner (Hayes and Wilson, 2008).

```tct_count_oe.py``` defines a set of functions for counting substrings (```count_many_substr()```), all trigrams (```trigram_counter()```), and for calculating observed-over-expected ratios based on these counts (```o_over_e_many_df()```). ```count_many_substr()``` has options that enable the user to only count word-initial strings, only onsets, as well as to count substrings on a given mapping tier -- e.g. to only at the cooccurrence of various kinds of stops within a word, while ignoring all other segments that might intervene.


### Corpora

-->

<!--Aymara-word-corpus
A word corpus of Aymara

Scripts are in the ```Scripts/``` folder, the ```Inputs/``` folder contains the input files, and the ```Outputs/``` folder contains the output files of the scripts. Within the ```Outputs/``` folder, the ```Outputs/Transcription/``` folder contains the transcription outputs - so far only complete for full words and the ```Outputs/Counts/``` folder contains raw counts (```Outputs/Counts/Raw```) of certain ngrams the list of matching words (```Outputs/Counts/Lists```) as well as observed-over-expected (O/E) values counted based on the raw counts (```Outputs/Counts/OE```).

The ```Scripts/languages.py``` file defines the class ```Language```, which is a systematic way of representing the sounds of a language. It allows for reference to natural classes within a language through attributes of a ```Language``` instance. The aymara sound system is also defined in the file as a variable. (Further attributes might be added to the class in the future depending on what languages will be implemented.)

The ```Scripts/ay_sp_en_filter.py``` file reads in three types of information: a set of Spanish words from text files in subfolders ([CORLEC Corpus](http://www.lllf.uam.es/ESP/Corlec.html): Marín, 1992), and a set of English ([CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict): Weide, 2005) and Aymara words ([An Crúbadán](http://crubadan.org/languages/ay): Scannell, 2007) from a file each. When read in, words are cleaned from numbers and non-alphanumeric characters, converted into lower case and 255 words were discarded because they contained a hyphen ("-"). The source file for Aymara (from Marín, 1992) was manually searched for apostrophe-related typos, 2 of them were corrected (_muru'q_ to _muruq'_ and _la'qa_ to _laq'a_).

The set of Aymara words are then cross-checked with both the Spanish and English words (in that order), and the words in the Aymara dictionary that match Spanish or English words are separated from the rest of the dataset, because they are presumable loan words. The script writes into three files: a filtered set of Aymara words with no Spanish or English loans in it (```Outputs/Aymara_words_no_sp_en.txt``` 81,325 unique word forms), the set of words that were filtered out because they appear in the Spanish word list as well (```Outputs/Spanish_loans.txt```, 188 words), and the set of words that were filtered out because they appear in the English word list as well (```Outputs/English_loans.txt```, 128 words) - the latter two sets might overlap. All words are lowercase.

```Scripts/ay_transcriber.py``` transcribes the ```Outputs/Aymara_words_no_sp_en.txt``` word list into IPA (International Phonetic Alphabet; ```Outputs/Transcription/aymara_ipa.txt```) and a transcription compatible with the UCLA Phonotactic Learner (Hayes and Wilson, 2008; ```Outputs/Transcription/aymara_pl.txt```), to which the definition of segments is in ```Outputs/Features.txt```. In addition, ```Scripts/ay_transcriber.py``` also generates a "pre-processed" file (```Outputs/Transcription/aymara_preprocessed.txt```), in which the representation of words is the same as their UCLA PL representation without spaces (i.e. sounds and representing unigrams are in one-to-one correspondence). A total of 11 words were discarded at this stage because of misplaced "'" characters - indicating ejectives. 1 because of missing vowel (_j'cha_), 3 because of ejectival closure between vowels (_cha'amañchistañapatakiwa_, _chu'uqi_, _chi'är_), 3 word forms had stops with both aspiration and ejectival closure (_kh'antatina_, _ph'ich'i_, _wichh'inqhapa_), and 4 word forms had ejectival closure marked in places where the only only adjacent consonant was not a stop (_huka'mp_, _arts'i_, _his'a_, _inamayayt'a'yi_). Words containing more than 2 adjacent instances of the same sound (e.g. 'aaa') were also removed. The resulting set of words was 81,206 mono- and polymorphemic Aymara word forms.

```Scripts/ay_delucca_rooter.py``` reads in a set of previously segmented word forms from the de Lucca dictionary (1987) and splits them into roots and suffixes. It then uses this list of suffixes and stems to eliminate non-root forms from the wordlist in the ```Outputs/Transcription/aymara_preprocessed.txt``` file. Words are eliminated if they start with a root from the de Lucca dictionary. Moreover, since roots in Aymara are typically 1-3 syllables long and there are no prefixes in the languages, words are reduced to their first 3 syllables. These 3-syllable substrings are then checked for word-final suffixes.

```Scripts/ay_counter.py``` contains various functions for counting relevant ngrams in the ```Outputs/Transcription/aymara_preprocessed.txt``` file for word forms and ```Inputs/delucca/ay_trans_roots_delucca.txt``` for roots. It can count instances of one ngram, multiple ones, with the options of only looking for word-initial matches and projecting on a certain tier. It outputs results into the ```Outputs/Counts/Raw/``` and ```Outputs/Counts/Lists/``` folders (for counts and list of matching words, respectively. (This file might be separated into a language-specific file - with a ```main()``` function only - and a general file that can be used in other corpora.)

```Scripts/ay_obs_over_exp.py``` counts observed-over-expected values on the outputs of ```ay_counter.py``` in ```Counts/Raw/``` for both word forms and roots with the use of the Ngram class and some functions defined in the file. (This file might be separated into a language-specific file - with a ```main()``` function only - and a general file that can be used in other corpora.)
-->


### References
Hayes, Bruce and Wilson, Colin. 2008. A maximum entropy model of phonotactics and phonotactic learning. _Linguistic inquiry_, 39(3), pp.379-440.

de Lucca, Manuel. 1987. _Diccionario practico aymara-castellano castellano-aymara_. Cochabamba:Los Amigos del Libro.

Marín, Marcos F. 1992. El Corpus Oral de Referencia de la Lengua Española contemporánea Project Report. Universidad Autónoma de Madrid. Available at <http://www.lllf.uam.es/ESP/Corlec.html> 

Scannell, Kevin P. 2007. The Crúbadán Project: Corpus building for under-resourced languages. _Building and Exploring Web Corpora: Proceedings of the 3rd Web as Corpus Workshop_. Vol. 4: pp.5-15.

Weide, Robert. _The Carnegie mellon pronouncing dictionary (cmudict. 0.6)_. Available at:  <http://www.speech.cs.cmu.edu/cgi-bin/cmudict> 2005.

