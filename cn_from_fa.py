import os
from utils import reverseComplement

def _copy_number(seq, repeat_unit):
    seq = seq.upper()

    repeat_length = len(repeat_unit)

    max_cn = 0

    while True:
        start_idx = seq.find(repeat_unit)

        if start_idx < 0:
            break

        s = seq[start_idx:]
        consecutive_run = 0

        while s.find(repeat_unit) == 0:
            consecutive_run += 1
            s = s[repeat_length:]

        max_cn = max(consecutive_run, max_cn)
        seq = seq[start_idx + 1:]

    return max_cn


def get_max_of_rc(repeat_unit, rc_repeat_unit, seq):
    return max(_copy_number(seq, repeat_unit), _copy_number(seq, rc_repeat_unit))


def get_copy_number(repeat_unit, fasta_file):
    assert repeat_unit is not None

    max_cn = 0

    if not os.path.isfile(fasta_file):
        return 'err'

    repeat_unit = repeat_unit.upper()
    rc_repeat_unit = reverseComplement(repeat_unit)

    with open(fasta_file) as fp:
        seq = ''

        for line in fp:
            if line.startswith('>'):
                if len(seq):
                    max_cn = max(max_cn, get_max_of_rc(repeat_unit, rc_repeat_unit, seq))

                seq = ''
                continue

            seq += line.strip()

        if len(seq):
            max_cn = max(max_cn, get_max_of_rc(repeat_unit, rc_repeat_unit, seq))

    return max_cn


def get_copy_number_dist(repeat_unit, fasta_file):
    assert repeat_unit is not None

    if not os.path.isfile(fasta_file):
        return {}

    repeat_unit = repeat_unit.upper()
    rc_repeat_unit = reverseComplement(repeat_unit)

    support = {}

    with open(fasta_file) as fp:
        seq = ''

        for line in fp:
            if line.startswith('>'):
                if len(seq):
                    cn = get_max_of_rc(repeat_unit, rc_repeat_unit, seq)
                    support[cn] = support.get(cn, 0) + 1

                seq = ''
                continue

            seq += line.strip()

        if len(seq):
            cn = get_max_of_rc(repeat_unit, rc_repeat_unit, seq)
            support[cn] = support.get(cn, 0) + 1

    return support

