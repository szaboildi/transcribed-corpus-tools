import os
import glob
import string

############################
# Reading in Spanish files #
############################
def extract_from_folders(folder):
    """
    Extracts lists of words from
    :param folder: folder in which documents are nested in subdirectories
    :return: a set of Spanish words
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


def main():
    folder = os.getcwd()
    spanish_folder = os.path.join(folder, "CORLEC\\")
    spanish_words = extract_from_folders(spanish_folder)

main()
