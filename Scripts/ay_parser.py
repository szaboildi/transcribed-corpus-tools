import os
import ay_transcriber as ay_trans
import ay_sp_en_filter as ay_filter

def main():
    words = ay_trans.set_reader(os.path.join(*[
        os.pardir, 'Outputs', 'Transcription',
        'aymara_preprocessed.txt']))
    roots = ay_trans.set_reader(os.path.join(*[
        os.pardir, 'Inputs', 'delucca', 'ay_roots_delucca_preprocessed.txt']))

    words_from_roots = {(word[:len(root)] + '+' + word[len(root):]).rstrip('+')
                        for word in words for root in roots
                        if word.startswith(root)}

    ay_filter.write_iter(words_from_roots, os.path.join(*[
        os.pardir, 'Outputs', 'Transcription',
        'aymara_dl_parsed_preprocessed.txt'
    ]))

    words_from_roots_pl = ay_trans.pl_trans(words_from_roots)
    ay_filter.write_iter(words_from_roots_pl, os.path.join(*[
        os.pardir, 'Outputs', 'Transcription',
        'aymara_dl_parsed_pl.txt'
    ]))


if __name__ == '__main__':
    main()