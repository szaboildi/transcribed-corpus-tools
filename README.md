# Aymara-word-corpus
A word corpus of Aymara

The ```Inputs``` folder contains the input files, the ```Outputs``` folder contains the output files of the scripts. Within the ```Outputs``` folder, the ```Transcription``` folder contains the transcription outputs - so far only of full words.

The ```ay_sp_en_filter.py``` file reads in three types of information: a set of Spanish words from text files in subfolders ([CORLEC Corpus](http://www.lllf.uam.es/ESP/Corlec.html): Marín, 1992), and a set of English ([CMU Pronouncing Dictionary](http://www.speech.cs.cmu.edu/cgi-bin/cmudict): Weide, 2005) and Aymara words ([An Crúbadán](http://crubadan.org/languages/ay): Scannell, 2007) from a file each. When read in, words are cleaned from numbers and non-alphanumeric characters.

The set of Aymara words are then cross-checked with both the Spanish and English words (in that order), and the words in the Aymara dictionary that match Spanish or English words are separated from the rest of the dataset, because they are presumable loan words. The script writes into three files: a filtered set of Aymara words with no Spanish or English loans in it (```Aymara_words_no_sp_en.txt``` 81,622 unique words), the set of words that were filtered out because they appear in the Spanish word list as well (```Spanish_loans.txt```, 188 words), and the set of words that were filtered out because they appear in the English word list as well (```English_loans.txt```, 128 words) - the latter two sets might overlap. All words are lowercase.

```ay_transcriber.py``` transcribes the ```Outputs/Aymara_words_no_sp_en.txt``` word list into IPA (International Phonetic Alphabet; ```Outputs/aymara_ipa.txt```) and a transcription compatible with the UCLA Phonotactic Learner (Hayes and Wilson, 2008; ```Outputs/aymara_pl.txt```), to which the definition of segments is in ```Features.txt```. In addition, ```ay_transcriber.py``` also generates a "pre-processed" file (```aymara_preprocessed.txt```), in which the representation of words is the same as their UCLA PL representation without spaces (i.e. sounds and representing unigrams are in one-to-one correspondence).

```ay_counts.py``` will contain functions for counting relevant bigrams or instances of regular expressions in the ```aymara_preprocessed.txt``` file. For now, it only contains basic functions and some variables.

# References
Hayes, Bruce and Wilson, Colin. 2008. A maximum entropy model of phonotactics and phonotactic learning. _Linguistic inquiry_, 39(3), pp.379-440.

Marín, Marcos F. 1992. El Corpus Oral de Referencia de la Lengua Española contemporánea Project Report. Universidad Autónoma de Madrid. Available at <http://www.lllf.uam.es/ESP/Corlec.html> 

Scannell, Kevin P. 2007. The Crúbadán Project: Corpus building for under-resourced languages. _Building and Exploring Web Corpora: Proceedings of the 3rd Web as Corpus Workshop_. Vol. 4: pp.5-15.

Weide, Robert. _The Carnegie mellon pronouncing dictionary (cmudict. 0.6)_. Available at:  <http://www.speech.cs.cmu.edu/cgi-bin/cmudict> 2005.
