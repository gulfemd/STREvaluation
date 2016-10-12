import os
from optparse import OptionParser
from cn_from_fa import get_copy_number
from utils import ddict, silentCall, reverseComplement


# executable paths
exe = ddict({})
exe.assembler = './executables/STRAssembly'


def run_assembler(sam_file, output_dir):
    silentCall([exe.assembler, '-sam', sam_file, '-out', output_dir])


def copy_number(metadata_file, fasta_file):
    repeat_unit = None

    with open(metadata_file) as fp:
        repeat_unit = fp.read().strip().split('\t')[-1]

    return get_copy_number(repeat_unit, fasta_file)


def extract(filename, path):
    str_id = filename[:-4]

    run_assembler(os.path.join(path, filename), path)

    cn = copy_number(os.path.join(path, (str_id + '.metadata')), os.path.join(path, (str_id + '.fa')))

    return (str_id, cn)


def main():
    parser = OptionParser()

    parser.add_option('-d', '--data')
    parser.add_option('-t', '--tsv')

    (options, args) = parser.parse_args()

    assert options.data
    assert options.tsv

    with open(options.tsv, 'w') as fp:
        print('STR\tCopy number', file=fp)

    for root, dirs, files in os.walk(options.data):
        for f in files:
            if not f.endswith('.sam'):
                continue

            str_id, cn = extract(f, root)

            with open(options.tsv, 'a') as fp:
                print(str_id + '\t' + str(cn), file=fp)


if __name__ == '__main__':
    main()
