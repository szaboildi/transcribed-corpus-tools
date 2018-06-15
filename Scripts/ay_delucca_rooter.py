import ay_sp_en_filter as ay_filter
import ay_transcriber as ay_trans
import os


def delucca_reader(path):
    """
    Reads in the delucca corpus into a dictionary
    :param path: path of the delucca dictionary
    :return: set of suffixes, set of roots
    """
    roots = set()
    suffixes = set()

    with open(path, 'r', encoding='utf-8') as delucca_f:
        for line in delucca_f:
            if ' ' in line:
                continue
            morphs = line.strip().split('-')
            morphs = [m.replace('(', '').replace(')', '') for m in morphs]

            if morphs[0] not in roots:
                roots.add(morphs[0])

            # I don't need exception handling for iterating over a
            ## potentially empty list, right?
            for morph in morphs[1:]:
                if morph not in suffixes:
                    suffixes.add(morph)

    return roots, suffixes



def main():
    roots, suffixes = delucca_reader(
        os.path.join(*[os.pardir, 'delucca', 'ay_delucca_segmented.txt']))
    ay_filter.write_iter(roots, os.path.join(*[
        os.pardir, 'delucca', 'ay_roots_delucca.txt']))
    ay_filter.write_iter(suffixes,os.path.join(*[
        os.pardir, 'delucca', 'ay_suffixes_delucca.txt']))

    lowering_table = ay_trans.make_lowering_table()
    roots_trans = ay_trans.transcribe(roots, lowering=lowering_table)
    suffixes_trans = ay_trans.transcribe(suffixes, lowering=lowering_table)
    ay_filter.write_iter(roots_trans, os.path.join(*[
        os.pardir, 'delucca', 'ay_trans_roots_delucca.txt']))
    ay_filter.write_iter(suffixes_trans, os.path.join(*[
        os.pardir, 'delucca', 'ay_trans_suffixes_delucca.txt']))


if __name__ == '__main__':
    main()

