import subprocess

class ddict(dict):
    '''Dot notation (c.attr) access to dictionary attributes.'''
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def silentCall(args):
    subprocess.call(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _complement(c):
    if c == 'A':
        return 'T'
    if c == 'T':
        return 'A'
    if c == 'C':
        return 'G'
    if c == 'G':
        return 'C'


def reverseComplement(seq):
    return ''.join(list(map(_complement, seq[::-1])))
