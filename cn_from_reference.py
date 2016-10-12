import os
import subprocess
from optparse import OptionParser
from utils import ddict
from cn_from_fa import get_copy_number


# executable paths
exe = ddict({})
exe.samtools = 'samtools' # system


def parseStr(s):
    c, pos = s.split('_')
    s, e = [int(x) for x in pos.split('-')]

    return (c, s, e)


def run_faidx(pos, fa_file):
    temp_fa_path = 'temp.regional.fa'

    with open(temp_fa_path, 'w') as fp:
        args = [exe.samtools, 'faidx', fa_file, pos]
        subprocess.call(args, stdout=fp)

    return temp_fa_path


def copy_number(str_id, metadata_file, fa_file):
    c, s, e = parseStr(str_id)

    repeat_unit = None
    with open(metadata_file) as fp:
        repeat_unit = fp.read().strip().split('\t')[-1]

    pos = c + ':' + str(s - len(repeat_unit)) + '-' + str(e + len(repeat_unit))

    temp_fa_path = run_faidx(pos, fa_file)

    return get_copy_number(repeat_unit, temp_fa_path)


def main():
    parser = OptionParser()

    parser.add_option('-d', '--data')
    parser.add_option('-f', '--fa')
    parser.add_option('-t', '--tsv')

    (options, args) = parser.parse_args()

    assert options.data
    assert options.fa
    assert options.tsv

    with open(options.tsv, 'w') as fp:
        print('STR\tCopy number', file=fp)

    for root, dirs, files in os.walk(options.data):
        for f in files:
            if not f.endswith('.metadata'):
                continue

            str_id = f[:-9]
            metadata_file_path = os.path.join(root, f)

            with open(options.tsv, 'a') as fp:
                cn = copy_number(str_id, metadata_file_path, options.fa)
                print(str_id + '\t' + str(cn), file=fp)


if __name__ == '__main__':
    main()
