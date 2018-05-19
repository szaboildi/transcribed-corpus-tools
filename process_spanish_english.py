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
        for subdir in glob.glob(os.path.join(dir, '*/')):
            for filename in glob.glob(os.path.join(subdir, '*.txt')):
                with open(filename, 'r') as f:
                    for line in f:
                        line = line.strip()
                        words = line.split(' ')
                        for word in words:
                            word = word.translate(None, string.punctuation)
                            if word.isalpha():
                                spanish_wordlist.append(word)

    return spanish_wordlist


def main():
    directory = os.path.dirname(os.getcwd())
    spanish_folder = os.path.join(directory, "CORLEC\\")
    print(spanish_folder)
    spanish_words = extract_from_folders(spanish_folder)
    print(spanish_words)

main()