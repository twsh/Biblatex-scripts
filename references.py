#!/usr/bin/env python3

import argparse
import logging
import re
from bibtexparser.bparser import BibTexParser
# Set logging level to ERROR and above;
# prevents bibtexparser giving a WARNING I don't care about.
logging.basicConfig(level=logging.ERROR)

# Match '@' followed by one or more letters, four numbers,
# then zero or more letters.
regex = '@[a-zA-Z]+\d{4}[a-zA-Z]*'
# Pandoc keys begin with '@'.
key_prefix = '@'

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    parser.add_argument('bibliography')
    parser.add_argument('--unused', '-u', action='store_true')
    args = parser.parse_args()
    target = args.target
    bibliography = args.bibliography
    with open(bibliography) as bib_file:
        set_of_keys =\
            {record['id'] for record in BibTexParser(bib_file.read()).entries}
    with open(target) as file:
        target_string = file.read()
        list_of_references = re.findall(regex, target_string)
        # The set needs to take out the beginning of pandoc keys.
        set_of_references =\
            {x.strip().lstrip(key_prefix) for x in list_of_references}
    if args.unused:
        unused = [x for x in set_of_keys if x not in set_of_references]
        if unused:
            print(
                'The following keys in {} were not used in {}:'.format(
                    bibliography,
                    target
                )
            )
            for reference in sorted(unused):
                print(reference)
    else:
        missing = [x for x in set_of_references if x not in set_of_keys]
        if missing:
            print(
                'The following references in {} were missing from {}:'.format(
                    target,
                    bibliography
                )
            )
            for reference in sorted(missing):
                print(reference)
