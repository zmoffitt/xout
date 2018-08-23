"""
Example program.

Usage:
    xout [--verbose | --quiet] <src> <dst>
    xout --version
    xout -h | --help

Options:

    -h, --help      Show this message
    --version       Print the version
    --quiet         No progress bar
    --verbose       Add debug info
"""

import sys
import signal
import os
from docopt import docopt
from tqdm import tqdm

from contextlib import contextmanager
from contextlib import redirect_stdout

@contextmanager
def dummy(ob):
    yield ob


# These should be 1 based
d = {
        5:  [6],
        7:  [7,13,14,15,17,18],
        8:  [10],
        10: [11,12],
        11: [6,7,8],
        15: [6,7,8],
        17: [5,7,9,11,13,15],
        18: [16,47],
        20: [8],
        21: [8],
        22: [8,9,10,11],
        24: [8],
}

def hasher(s):
    return len(s) * 'X'


def sigpipe():
    # Reset Python's default SIGPIPE handler for Linux
    signal.signal(signal.SIGPIPE, signal.SIG_DFL)

def cli(src, dst, verbose=False, quiet=False):
    is_file  = True if src != '-' else False
    filename = src if is_file else 'stdin'
    nbytes   = os.stat(src).st_size if is_file else -1

    # If destination is a folder instead of a directory
    # then amend path with filename.bak
    if os.path.isdir(dst):
        dst = os.path.join(dst, os.path.basename(src) + '.bak')

    if (verbose):
        print(src, dst, file=sys.stderr)
        print(nbytes, is_file, filename, file=sys.stderr)

    source = open(src, 'r') if is_file else sys.stdin
    dest   = sys.stdout if dst == '-' else open(dst, 'w')

    with source, dest:
        if nbytes > 0:
            with tqdm(desc=filename, disable=quiet, total=nbytes, unit=" bytes", unit_scale=True) as bar:
                for lineno, line in enumerate(source):
                    filter_line(line, dest)
                    bar.update(len(line))
        else:
            mm = enumerate(tqdm(lines, disable=quiet, desc=filename, unit=" lines", unit_scale=True))
            for lineno, line in mm:
                filter_line(line, dest)


def filter_line(line, output):
    # remove trailing newline
    line = line.strip()

    try:
        # Each record is delimited by a pipe |
        line_a = line.split('|')

        # First field in each line is the 2 digit "record type"
        record_type = int(line_a[0])

        if record_type in d:
            pii_a = [hasher(f) if ind+1 in d[record_type] else f for ind, f in enumerate(line_a)]
            pii   = '|'.join(pii_a)
            print(pii, file=output)
        else:
            print(pii, file=output)
    except:
        # if the line isn't in the expected form, pass it on unchanged
        print(line, file=output)

def main():
    sigpipe()

    args = docopt(__doc__, version='1.0')
    if args['--verbose']:
        print(args)
    cli(args['<src>'], args['<dst>'], args['--verbose'], args['--quiet'])

if __name__ == '__main__':
    main()

