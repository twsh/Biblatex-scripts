#!/usr/bin/env python3

import argparse

from bibtexparser.bparser import BibTexParser

entry_types_to_reference_types =\
    {
        'inbook': ['book', 'mvbook'],
        'incollection': ['collection', 'mvcollection'],
        'inproceedings': ['proceedings']
    }

crossref_types = sorted([key for key in entry_types_to_reference_types])


def make_list(strings, delimiter='or'):
    """
    Take a list of strings and a string.
    If the length of the string is 1 return its element.
    If it's 2, return its elements joined by the delimeter.
    Otherwise, return its elements joined by commas (',') with
    the delimeter before the final element.
    Default to 'or' for delimiter.
    >>> make_list(['foo'])
    'foo'
    >>> make_list(['foo', 'bar'])
    'foo or bar'
    >>> make_list(['foo', 'bar'], 'and')
    'foo and bar'
    >>> make_list(['foo', 'bar', 'zip'])
    'foo, bar, or zip'
    """
    if len(strings) == 1:
        return strings[0]
    elif len(strings) == 2:
        return strings[0] + ' ' + delimiter + ' ' + strings[1]
    else:
        return ', '.join(strings[:-1]) + ', ' + delimiter + ' ' + strings[-1]


def bib_to_string(bibliography):
    """ dict of dict -> str
    Take a biblatex bibliography represented as a dictionary
    and return a string representing it as a biblatex file.
    """
    string = ''
    for entry in bibliography:
        string += '\n@{}{{{},\n'.format(
            bibliography[entry]['type'],
            bibliography[entry]['id']
        )
        for field in bibliography[entry]:
            if field != 'id' and field != 'type':
                string += '\t{} = {{{}}},\n'.format(
                    field,
                    bibliography[entry][field]
                )
        string = string[:-2] + '}\n'
    return string

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('bibliography')
    parser.add_argument('--expand', action='store_true')
    args = parser.parse_args()
    bibliography = args.bibliography
    with open(bibliography) as bib_file:
        entries = BibTexParser(
            bib_file.read(),
            ignore_nonstandard_types=False
        ).entries_dict
    for entry in entries:
        # Find the entries with a crossref field
        if 'crossref' in entries[entry]:
            entry_crossref = entries[entry]['crossref']
            entry_id = entries[entry]['id']
            entry_type = entries[entry]['type']
            # Check entries for crossref fields that don't match another entry
            if entry_crossref not in entries:
                print(
                    '{} referenced by {} was not found.'.format(
                        entry_crossref,
                        entry_id
                    )
                )
            else:
                # Check that the type of the entry matches
                # the type of what it references
                if entry_type in entry_types_to_reference_types:
                    allowed_types = entry_types_to_reference_types[entry_type]
                    entry_crossref_type = entries[entry_crossref]['type']
                    if entry_crossref_type\
                            not in allowed_types:
                        print(
                            "The type of {} referenced by {} is {}. "
                            "It should probably be {}.".format(
                                entry_crossref,
                                entry_id,
                                entry_crossref_type,
                                make_list(allowed_types)
                            )
                        )
            # Check that only expected types have crossref fields
            if entry_type not in crossref_types:
                print(
                    "The type of {} is {}. "
                    "That's not one of the types expected to have a crossref, "
                    "which are: {}.".format(
                        entry_id,
                        entry_type,
                        make_list(crossref_types)
                    )
                )
    if args.expand:
        crossrefs = set()
        leave =\
            [
                'id',
                'type',
                'read',
                'bdsk-file-1',
                'doi',
                'date-added',
                'date-modified'
            ]
        for entry in entries:
            if 'crossref' in entries[entry]:
                crossref = entries[entry]['crossref']
                crossrefs.add(crossref)
                for field in entries[crossref]:
                    if field == 'title':
                        entries[entry]['booktitle'] = entries[crossref]['title']
                    elif field == 'subtitle':
                        entries[entry]['booksubtitle'] =\
                            entries[crossref]['subtitle']
                    elif field in leave:
                        pass
                    else:
                        entries[entry][field] = entries[crossref][field]
                del entries[entry]['crossref']
        if crossrefs:
            for key in crossrefs:
                del entries[key]
            with open(bibliography, 'w') as bib_file:
                bib_file.write(bib_to_string(entries))
            print(
                'I found the following crossrefs: {}.'
                'I expanded them, and then deleted the originals.'.format(
                    ', '.join(sorted(list(crossrefs)))
                )
            )
