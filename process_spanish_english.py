import os
import glob
import string

############################
# Reading in Spanish files #
############################
# Reading in the Spanish dictionary from subfolders
def extract_from_folders(folder):
    """
    Extracts lists of words from subfolders
    :param folder: folder in which documents are nested in subdirectories
    :return: a set of Spanish words (no frequency)
    """
    spanish_wordlist = []
    for dir in glob.glob(os.path.join(folder, '*/')):
        for filename in glob.glob(os.path.join(dir, '*.txt')):
            with open(filename, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    words = line.split(' ')
                    for word in words:
                        to_remove = string.punctuation
                        table = {ord(char): None for char in to_remove}
                        word = word.translate(table)
                        if word.isalpha():
                            spanish_wordlist.append(word)

    return spanish_wordlist


# Reading in the CMU file
def cmu_reader(filename):
    """
    Reads in the CMU file into a dictionary of spelling-to-pronunciation
    :param filename: name & path of the CMU file
    :return: a list of English words (no frequency)
    """
    cmu = []
    with open(filename, 'r') as cmu_f:
        for line in cmu_f:
            line = line.strip()
            bits = line.split(',')
            spelling = bits[0].strip('"')
            if spelling not in cmu:
                cmu.append(spelling)

    return cmu


def main():
    folder = os.getcwd()
    spanish_folder = os.path.join(folder, "CORLEC\\")
    spanish_words = extract_from_folders(spanish_folder)
    cmu_path = 'cmu_dictionary.txt'
    cmu = cmu_reader(cmu_path)

main()
