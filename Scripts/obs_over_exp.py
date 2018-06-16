import os
import itertools

# Counts observed over expected values
class Bigrams():
    def __init__(self, name, first, second, frequency):
        self.name = name
        self.first = first
        self.second = second
        self.frequency = frequency

    def O_over_E(self, as_first, as_second, general_gram):
        pass


# Read in the bigrams
def read_bigrams(path, middle=''):
    """
    Reads in a file as a set of bigrams
    :param path: Where the file is
    :param middle: What character is in the middle
    :return: Set of bigrams
    """
    set_of_bigrams = set()
    with open(path, 'r', encoding='utf-8') as in_f:
        for line in in_f:
            if middle in line.lower() and not line.startswith('stop'):
                bits = line.strip().replace('plain stop', 'plain').split('\t')
                characters = bits[0].split(' ')
                name = ''
                for ch in characters:
                    if ch.lower() == middle:
                        name += 'X'
                    else:
                        name += ch[0].upper()
                name = Bigrams(name=name, first=name[0], second=name[-1], frequency=int(bits[1]))
                set_of_bigrams.add(name)

    return set_of_bigrams


def o_over_e(bigram_set, first, second):
    """
    Counts an observed-over-expected (O/E) ratio.
    :param bigram_set: Set of bigrams with their counts
    :param first: First segment of the bigram
    :param second: Second segment of the bigram
    :return: The O/E ratio
    """
    total_count = sum({bigram.frequency for bigram in bigram_set})

    target_set = {bigram for bigram in bigram_set
                  if bigram.first == first and bigram.second == second}

    observed = sum({bigram.frequency for bigram in target_set})

    first_set = {bigram for bigram in bigram_set
                 if bigram.first == first}
    second_set = {bigram for bigram in bigram_set
                  if bigram.second == second}
    first_prob = sum({bigram.frequency for bigram in first_set}) / total_count
    second_prob = sum({bigram.frequency for bigram in second_set}) / total_count
    try:
        o_e = observed / (first_prob * second_prob * total_count)
    except:
        o_e = 'One part of the denominator is 0.\n' \
               'First prob = {}\n' \
               'Second prob = {}\n' \
               'Total count = {}'.format(str(first_prob),
                                         str(second_prob),
                                         str(total_count))
    return o_e


def main():
    sxs_counts = read_bigrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'aymara_counts_stop_x_stop.txt']),
                              middle="anything")
    svs_counts = read_bigrams(os.path.join(*[
        os.pardir, 'Outputs', 'Counts', 'aymara_counts_stop_x_stop.txt']),
                              middle="vowel")

    combinations = itertools.product(['A', 'E', 'P'], ['A', 'E', 'P'])
    o_e_table = {}
    for combo in combinations:
        o_e_table[combo] = o_over_e(sxs_counts, *combo)
        print(str(combo) + ' ' + str(o_over_e(sxs_counts, *combo)))

    # print(o_e_table)

if __name__ == '__main__':
    main()