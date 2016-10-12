import os
import subprocess
from optparse import OptionParser
from utils import ddict
from cn_from_fa import get_copy_number


# executable paths
exe = ddict({})
exe.samtools = 'samtools' # system


def indexRemap(remap_file):
    strs = {}

    with open(remap_file) as fp:
        next(fp)

        for line in fp:
            row = line.strip().split('\t')
            c = row[1][3:]
            s = int(row[2]) + 1
            e = int(row[3])

            str_id = str(c) + '_' + str(s) + '-' + str(e)
            strs[str_id] = row[-3:] + [row[7]]

    return strs


def run_faidx(pos, fa_file):
    temp_fa_path = 'temp.regional.fa'

    with open(temp_fa_path, 'w') as fp:
        args = [exe.samtools, 'faidx', fa_file, pos]
        subprocess.call(args, stdout=fp)

    return temp_fa_path


def copy_number(strs, s, fa_file):
    if s not in strs:
        return 'no-remap-data'

    metadata = strs[s]
    repeat_unit = metadata[3]

    pos = metadata[2] + ':' + str(int(metadata[0]) - len(repeat_unit)) + '-' + str(int(metadata[1]) + len(repeat_unit))

    temp_fa_path = run_faidx(pos, fa_file)

    return get_copy_number(repeat_unit, temp_fa_path)


def main():
    parser = OptionParser()

    parser.add_option('-s', '--str')
    parser.add_option('-f', '--fa')
    parser.add_option('-r', '--remap')
    parser.add_option('-t', '--tsv')

    (options, args) = parser.parse_args()

    assert options.str
    assert options.fa
    assert options.remap
    assert options.tsv

    with open(options.tsv, 'w') as fp:
        print('STR\tCopy number', file=fp)

    strs = indexRemap(options.remap)

    with open(options.str) as fp:
        next(fp)

        for line in fp:
            str_id, _ = line.strip().split('\t')

            with open(options.tsv, 'a') as ofp:
                cn = copy_number(strs, str_id, options.fa)
                print(str_id + '\t' + str(cn), file=ofp)


if __name__ == '__main__':
    main()
