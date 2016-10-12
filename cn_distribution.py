import os
from optparse import OptionParser
from cn_from_fa import get_copy_number_dist


def copy_number(metadata_file, fasta_file):
    repeat_unit = None

    with open(metadata_file) as fp:
        repeat_unit = fp.read().strip().split('\t')[-1]

    return get_copy_number_dist(repeat_unit, fasta_file)


def get_distribution(filename, path):
    str_id = filename[:-9]

    d = copy_number(os.path.join(path, filename), os.path.join(path, (str_id + '.fa')))

    return (str_id, d)


def main():
    parser = OptionParser()

    parser.add_option('-d', '--data')
    parser.add_option('-t', '--tsv')

    (options, args) = parser.parse_args()

    assert options.data
    assert options.tsv

    with open(options.tsv, 'w') as fp:
        print('STR\tCopy number\tCopy number support\t...', file=fp)

    for root, dirs, files in os.walk(options.data):
        for f in files:
            if not f.endswith('.metadata'):
                continue

            str_id, d = get_distribution(f, root)

            row = [str_id]

            for c in sorted(d, reverse=True):
                row.append(str(c))
                row.append(str(d[c]))

            with open(options.tsv, 'a') as fp:
                print('\t'.join(row), file=fp)


if __name__ == '__main__':
    main()
