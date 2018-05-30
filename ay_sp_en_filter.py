#!/usr/bin/python
import os
import glob
import string

########################
# Reading in wordlists #
########################
## Reading in the Spanish dictionary from subfolders
def extract_from_folders(folder):
    """
    Extracts a set of words from files in subfolders, removes punctuation
    :param folder: folder in which documents are nested in subdirectories
    :return: a set of Spanish words (no frequency)
    """
    spanish_wordlist = set()
    to_remove = string.punctuation
    table = {ord(char): None for char in to_remove}

    for dir in glob.glob(os.path.join(folder, '*/')):
        for filename in glob.glob(os.path.join(dir, '*.txt')):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    words = line.split(' ')
                    for word in words:
                        word = word.translate(table)
                        word = word.lower()
                        if word.isalpha():
                            spanish_wordlist.add(word)

    return spanish_wordlist


## Reading in the CMU file
def cmu_reader(filename):
    """
    Reads in the CMU file into a set of English words
    :param filename: name & path of the CMU file
    :return: a set of English words (no frequency)
    """
    with open(filename, 'r') as cmu_f:
        cmu = {line.strip().split(',')[0].strip('"').lower() for line in cmu_f}

    return cmu


## Reading in Aymara word list
def aymara_reader(filename):
    """
    Reads in an Aymara word list and returns a list with the words,
    removes punctuation, except for "'"
    :param filename: name & path of the Aymara word list
    :return: a list of Aymara words (no frequency)
    """
    to_remove = '"():;.,?!^'
    table = {char: "" for char in to_remove}
    table["’"] = "'"
    # print(table)
    with open(filename, 'r', encoding='utf-8') as aym_f:
        interim_aym = {line.split(' ')[1].strip().lower().translate(table) for line in aym_f}
        aym = {word for word in interim_aym if
               not any(char.isdigit() for char in word) and \
               '@' not in word}

    return aym


#########################
# Filtering and writing #
#########################
"""
## Filtering lists with lists
def filter_lst(filter_from, stoplist):

    Filters out words appearing in the stoplist from another list
    :param filter_from: the list that should be filtered
    :param stoplist: the list of words that should be filtered
                     from the other list
    :return: two lists: the list of words that were filtered out
             and the list of words that were not

    pass_list = [item for item in filter_from if item in stoplist]
    discard_list = [item for item in filter_from if item in stoplist]

    return pass_list, discard_list
"""

## Writing output lists to files
def write_list(lst, path):
    """
    Writes list of words to file.
    :param lst: list to be written to file
    :param path: path of new file
    :return: None
    """
    with open(path, 'w', encoding='utf-8') as output_w:
        for item in lst:
            output_w.write(item + '\n')


def main():
    # Reading in files
    folder = os.getcwd()
    spanish_folder = os.path.join(folder, "Inputs\\CORLEC\\")
    sp = extract_from_folders(spanish_folder)
    cmu_path = "Inputs\\cmu_dictionary.txt"
    en = cmu_reader(cmu_path)
    aym_path = "Inputs\\ay-freq.txt"
    aym = aymara_reader(aym_path)

    # Filtering
    sp_disc = aym - (aym - sp)
    write_list(sp_disc, "Outputs\\Spanish_loans.txt")
    en_disc = aym - (aym - en)
    write_list(en_disc, "Outputs\\English_loans.txt")
    no_sp_en = aym - sp - en
    write_list(no_sp_en, "Outputs\\Aymara_words_no_sp_en.txt")

if __name__ == "__main__":
    main()