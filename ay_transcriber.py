# Reading in the word list
def list_reader(filename):
    """
    Reads in file into list.
    :param filename: location of text file with one word/line
    :return: a list of words
    """
    lst = []
    with open(filename, 'r', encoding='utf-8') as f:
        for line in f:
            word = line.strip()
            word = word.lower()
            if word.isalpha() and word not in lst:
                lst.append(word)

    return lst


# Rules in Aymara
## Transcription:
def transcribe(wrd):
    vowels = {''}
    trans1 = {'ch':'c',
              'ñ':'N',
              'j': 'H'}
    trans2 = {'y':'j',
              'h':'H'}
    trans3 = {'ll':'y'}
### ll -> alveo-palatal lateral
### ch -> c
### ñ -> N
### j -> h
### y -> j
## Sibilant: S after ch-series, y and N
## ch -> s/S before /t/
## Vowel assimilation
## Vowel length

def main():
    ay_orth = list_reader("Outputs\\Aymara_words_no_sp_en.txt")