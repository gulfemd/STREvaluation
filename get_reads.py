import os
import shutil
from optparse import OptionParser
from utils import silentCall, ddict


# executable paths
exe = ddict({})
exe.targetedReadFinder = './executables/targeted-read-finder'


def run_finder(str_file, bam_file, output_dir):
    bam_file_name = os.path.basename(bam_file)[:-4]
    out = os.path.join(output_dir, bam_file_name)

    if os.path.exists(out):
        shutil.rmtree(out)

    os.makedirs(out)

    silentCall([exe.targetedReadFinder, '--bam', bam_file, '--str', str_file, '--out', out])


def main():
    parser = OptionParser()

    parser.add_option('-s', '--str')
    parser.add_option('-b', '--bam', action='append')
    parser.add_option('-o', '--out')

    (options, args) = parser.parse_args()

    assert options.str
    assert options.bam
    assert options.out

    for b in options.bam:
        run_finder(options.str, b, options.out)


if __name__ == '__main__':
    main()
