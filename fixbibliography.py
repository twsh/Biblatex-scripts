#!/usr/bin/env python3

import argparse
import re
import sys


def fix_keys(l):
    """ list -> list
    Take a list that represents lines.
    Find lines which is the start of a bibtex entry without a key.
    Add dummy keys to those lines.
    >>> fix_keys(
        ['@article{\n', '    Author = {Thomas Hodgson}\n', '}\n']
    )
    ['@article{Foo1,\n', '    Author = {Thomas Hodgson}\n', '}\n']
    """
    i = 1
    j = 0
    while j < len(l):
        if re.match('@\\w+{,{0,1}$', l[j].strip()):
            l[j] = l[j][:l[j].find('{')+1] + 'Foo' + str(i) + ',' + '\n'
            i += 1
        j += 1
    return l

# The script will look for positional arguments.
# The first it finds will be the input, and the second will be the output.
# Defaults are stdin and stdout, respectively.
# This means that if the input is read from a file the output must be stdout.

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'input',
        nargs='?',
        type=argparse.FileType('r'),
        default=sys.stdin
    )
    parser.add_argument(
        'output',
        nargs='?',
        type=argparse.FileType('w'),
        default=sys.stdout
    )
    args = parser.parse_args()
    content = args.input.readlines()
    # Is the first line anything other than a new line?
    # If so, insert one
    if content[0] != '\n':
        content.insert(0, '\n')
    # Provide dummy citekeys
    content = fix_keys(content)
    output = ''.join(content)
    args.output.write(output)
