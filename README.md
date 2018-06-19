# Aymara-word-corpus
A word corpus of Aymara

Scripts are in the ```Scripts``` folder, the ```Inputs``` folder contains the input files, and the ```Outputs``` folder contains the output files of the scripts. Within the ```Outputs``` folder, the ```Transcription``` folder contains the transcription outputs - so far only complete for full words.

The ```languages.py``` file defines the class ```Language```, which is a systematic way of representing the sounds of a language. It allows for reference to natural classes within a language through attributes of a ```Language``` instance. The aymara sound system is also defined in the file as a variable. (Further attributes might be added to the class in the future depending on what languages will be implemented.)

The ```ay_sp_en_filter.py``` file reads in three types of information: a set of Spanish words from text files in subfolders ([CORLEC Corpus](http://www.lllf.uam.es/ESP/Corlec.html): Marín, 1992), and a set of English ([CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict): Weide, 2005) and Aymara words ([An Crúbadán](http://crubadan.org/languages/ay): Scannell, 2007) from a file each. When read in, words are cleaned from numbers and non-alphanumeric characters, from the Aymara corpus 255 words were discarded because they contained a hyphen ("-"). The source file for Aymara (from Marín, 1992) was manually searched for apostrophe-related typos, 2 of them were corrected (_muru'q_ to _muruq'_ and _la'qa_ to _laq'a_).

The set of Aymara words are then cross-checked with both the Spanish and English words (in that order), and the words in the Aymara dictionary that match Spanish or English words are separated from the rest of the dataset, because they are presumable loan words. The script writes into three files: a filtered set of Aymara words with no Spanish or English loans in it (```Aymara_words_no_sp_en.txt``` 81,368 unique word forms), the set of words that were filtered out because they appear in the Spanish word list as well (```Spanish_loans.txt```, 188 words), and the set of words that were filtered out because they appear in the English word list as well (```English_loans.txt```, 128 words) - the latter two sets might overlap. All words are lowercase.

```ay_transcriber.py``` transcribes the ```Outputs/Aymara_words_no_sp_en.txt``` word list into IPA (International Phonetic Alphabet; ```Outputs/aymara_ipa.txt```) and a transcription compatible with the UCLA Phonotactic Learner (Hayes and Wilson, 2008; ```Outputs/aymara_pl.txt```), to which the definition of segments is in ```Features.txt```. In addition, ```ay_transcriber.py``` also generates a "pre-processed" file (```aymara_preprocessed.txt```), in which the representation of words is the same as their UCLA PL representation without spaces (i.e. sounds and representing unigrams are in one-to-one correspondence). A total of 11 words were discarded at this stage because of misplaced "'" characters - indicating ejectives. 1 because of missing vowel (_j'cha_), 3 because of ejectival closure between vowels (_cha'amañchistañapatakiwa_, _chu'uqi_, _chi'är_), 3 word forms had stops with both aspiration and ejectival closure (_kh'antatina_, _ph'ich'i_, _wichh'inqhapa_), and 4 word forms had ejectival closure marked in places where the only only adjacent consonant was not a stop (_huka'mp_, _arts'i_, _his'a_, _inamayayt'a'yi_). The resulting set of words was 81,266 mono- and polymorphemic Aymara word forms.

```ay_counter.py``` contains various functions for counting relevant ngrams in the ```aymara_preprocessed.txt``` file. It can count instances of one ngram, multiple ones, with the options of only looking for word-initial matches and projecting on a certain tier. It outputs results into the ```Outputs/Counts/Raw``` and ```Outputs/Counts/Lists``` folders (for counts and list of matching words, respectively. (This file might be separated into a language-specific file - with a ```main()``` function only - and a general file that can be used in other corpora.)

```ay_obs_over_exp.py``` counts observed-over-expected values with the use of the Ngram class and some functions defined in the file. (This file might be separated into a language-specific file - with a ```main()``` function only - and a general file that can be used in other corpora.)


# References
Hayes, Bruce and Wilson, Colin. 2008. A maximum entropy model of phonotactics and phonotactic learning. _Linguistic inquiry_, 39(3), pp.379-440.

Marín, Marcos F. 1992. El Corpus Oral de Referencia de la Lengua Española contemporánea Project Report. Universidad Autónoma de Madrid. Available at <http://www.lllf.uam.es/ESP/Corlec.html> 

Scannell, Kevin P. 2007. The Crúbadán Project: Corpus building for under-resourced languages. _Building and Exploring Web Corpora: Proceedings of the 3rd Web as Corpus Workshop_. Vol. 4: pp.5-15.

Weide, Robert. _The Carnegie mellon pronouncing dictionary (cmudict. 0.6)_. Available at:  <http://www.speech.cs.cmu.edu/cgi-bin/cmudict> 2005.
