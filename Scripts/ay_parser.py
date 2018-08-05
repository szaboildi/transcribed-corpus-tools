import os
import ay_transcriber as ay_trans
import tct_utility as uti
from tct_languages import aymara as ay


def main():
    words = uti.set_reader(os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_preprocessed.txt']))
    roots = uti.set_reader(os.path.join(*[
        os.pardir, 'Aymara', 'Inputs', 'delucca',
        'ay_roots_delucca_preprocessed.txt']))

    words_from_roots = {(word[:len(root)] + '+' + word[len(root):]).rstrip('+')
                        for word in words for root in roots
                        if word.startswith(root)}

    uti.write_iter(words_from_roots, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_dl_parsed_preprocessed.txt'
    ]))
    words_from_roots_pl = ay_trans.pl_trans(words_from_roots)
    uti.write_iter(words_from_roots_pl, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_dl_parsed_pl.txt'
    ]))


    words_from_roots_ej = {ay_trans.nth_transcribe(word, ay.ejectives) for word in words_from_roots}
    uti.write_iter(words_from_roots_ej, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_dl_parsed_preprocessed_ejectives.txt'
    ]))
    words_from_roots_ej_pl = ay_trans.pl_trans(words_from_roots_ej)
    uti.write_iter(words_from_roots_ej_pl, os.path.join(*[
        os.pardir, 'Aymara', 'Outputs', 'Transcription',
        'aymara_dl_parsed_pl_ejectives.txt'
    ]))


if __name__ == '__main__':
    main()