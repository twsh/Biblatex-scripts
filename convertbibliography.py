#!/usr/bin/env python3

import argparse
import re
import shutil
import titlecase

from bibtexparser.bparser import BibTexParser
from bibtexparser.bwriter import to_bibtex
from bibtexparser.customization import *


words_to_numerals =\
    {
        'first': '1',
        'second': '2',
        'third': '3',
        'fourth': '4',
        'fifth': '5',
        'sixth': '6',
        'seventh': '7',
        'eighth': '8',
        'ninth': '9',
        'tenth': '10'
    }


def title_name(name):
    """
    str -> str
    Take a name and return it in title case, leaving 'and' alone.
    >>> title_name('hodgson, thomas')
    'Hodgson, Thomas'
    >>> title_name('hodgson, thomas and JANE, DOE')
    'Hodgson, Thomas and Doe, Jane'
    """
    name =\
        ' '.join(
            [x.title() if not re.match('and', x) else x for x in name.split()]
        )
    return name


def titlecase_name(record):
    """
    Put authors and editors into title case.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "author" in record:
        record["author"] = title_name(record["author"])
    if "editor" in record:
        record["editor"] = title_name(record["editor"])
    return record


def publisher(record):
    """
    Protect 'and' in publisher field with braces around the field.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "publisher" in record:
        if re.search('and', record["publisher"]):
            record["publisher"] = hodgson.braces(record["publisher"])
    return record


def edition(record):
    """
    Put "Edition" in a nice format.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "edition" in record:
        if record["edition"].lower().strip() in words_to_numerals:
            record["edition"] =\
                words_to_numerals[record["edition"].lower().strip()]
        elif re.search('\d+(st|nd|rd|th)', record["edition"].lower().strip()):
            record["edition"] =\
                re.sub('(st|nd|rd|th)', '', record["edition"].lower().strip())
    return record


def journaltitle(record):
    """
    Change "Journal" to "Journaltitle".

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "journal" in record:
        record["journaltitle"] = record["journal"]
        del record["journal"]
    return record


def case_title(record):
    """
    Put titles in titlecase.
    Depends on the 'titlecase' module
    https://pypi.python.org/pypi/titlecase/

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "title" in record:
        record["title"] = titlecase.titlecase(record["title"])
    if "subtitle" in record:
        record["subtitle"] = titlecase.titlecase(record["subtitle"])
    if "booktitle" in record:
        record["booktitle"] = titlecase.titlecase(record["booktitle"])
    return record


def join_author(record):
    """
    Convert authors as lists of strings to strings joined by "and".

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "author" in record:
        record["author"] = " and ".join(record["author"])
    return record


def booktitle(record):
    """
    Add 'Booktitle' field identical to 'Title' field for book entries.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if record["type"] == "book":
        if "title" in record:
            record["booktitle"] = record["title"]
    return record


def remove_abstract(record):
    """
    Remove abstracts.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "abstract" in record:
        del record["abstract"]
    return record


def remove_ISSN(record):
    """
    Remove ISSN.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "issn" in record:
        del record["issn"]
    return record


def remove_ISBN(record):
    """
    Remove ISBNs.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "isbn" in record:
        del record["isbn"]
    return record


def remove_copyright(record):
    """
    Remove copyright.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "copyright" in record:
        del record["copyright"]
    return record


def remove_language(record):
    """
    Remove languages.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "language" in record:
        del record["language"]
    return record


def remove_publisher(record):
    """
    Remove publisher.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if record["type"] == "article":
        if "publisher" in record:
            del record["publisher"]
    return record


def remove_link(record):
    """
    Remove abstracts.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "link" in record:
        del record["link"]
    return record


def remove_ampersand(record):
    """
    Convert ampersand ('&') to 'and'

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "booktitle" in record:
        record["booktitle"] = re.sub('\\\\&', 'and', record["booktitle"])
    if "journaltitle" in record:
        record["journaltitle"] = re.sub('\\\\&', 'and', record["journaltitle"])
    if "subtitle" in record:
        record["subtitle"] = re.sub('\\\\&', 'and', record["subtitle"])
    if "title" in record:
        record["title"] = re.sub('\\\\&', 'and', record["title"])
    return record


def escape_characters(record):
    """
    Make sure that characters reserved by LaTeX are escaped

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    list_of_characters = ['&', '%', '_']
    for val in record:
        for c in list_of_characters:
            record[val] = re.sub(
                '(?<!\\\\){}'.format(c),
                '\{}'.format(c),
                record[val]
            )
    return record


def jstor(record):
    """
    Get rid of JSTOR's special fields.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "jstor_articletype" in record:
        del record["jstor_articletype"]
    if "jstor_formatteddate" in record:
        del record["jstor_formatteddate"]
    if "jstor_issuetitle" in record:
        del record["jstor_issuetitle"]
    return record


def remove_pp(record):
    """
    Get rid of 'p[.]'/'pp[.]' at the start of a pages field.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "pages" in record:
        record["pages"] = re.sub('[Pp]{1,2}\\.?', '', record["pages"]).strip()
    return record


def protect(s):
    """
    Str -> Str

    Helper function for `protect_capitalization`.
    Take a string and return a string where words starting with capital letters
    (after the first word) are capitalised.
    """
    l = s.split()
    return l[0] + ' ' + ' '.join(
        ['{' + x + '}' if x[0].isupper() else x for x in l[1:]]
    )


def protect_capitalisation(record):
    """
    Protect capitalised words with braces.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "title" in record:
        record["title"] = protect(record["title"])
    if "subtitle" in record:
        record["subtitle"] = protect(record["subtitle"])
    if "booktitle" in record:
        record["booktitle"] = protect(record["booktitle"])
    return record


def multivolume(record):
    """
    If a book or collection has a volume number,
    change its type to mvbook/mvcollection.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if record["type"] == "book":
        if "volume" in record:
            record["type"] = "mvbook"
    elif record["type"] == "collection":
        if "volume" in record:
            record["type"] = "mvcollection"
    return record


def remove_booktitle(record):
    """
    Remove abstracts.

    :param record: the record.
    :type record: dict
    :returns: dict -- the modified record.
    """
    if "booktitle" in record:
        del record["booktitle"]
    return record


def customizations(record):
    """Use some functions delivered by the library

    :param record: a record
    :returns: -- customized record
    """
    record = author(record)
    record = join_author(record)
    record = titlecase_name(record)
    record = case_title(record)
    record = convert_to_unicode(record)
    record = journaltitle(record)
    record = page_double_hyphen(record)
    record = remove_pp(record)
    record = escape_characters(record)
    record = remove_ampersand(record)
    record = edition(record)
    record = multivolume(record)
    record = publisher(record)
    return record

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('target')
    args = parser.parse_args()
    target = args.target
    list_of_extensions = ['bib']
    bib = hodgson.check_extensions(target, list_of_extensions)
    # The bib file to modify
    shutil.copy(bib, bib + '.backup')
    print(
        "I have made a backup of the orignal file at {}.backup"
        .format(bib)
    )
    with open(bib) as biblatex:
        bibliography = BibTexParser(
            biblatex.read(),
            customization=customizations,
            ignore_nonstandard_types=False
            # Otherwise bibtexparser will complain if I give it a collection
        )
    with open(bib, 'w') as biblatex:
        biblatex.write(to_bibtex(bibliography))