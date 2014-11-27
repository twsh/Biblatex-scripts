# crossrefs.py

Biblatex uses a 'crossref' field to link entries together. For example a chapter in an edited volume will be of type 'incollection' and have a crossref to an entry of type 'collection'. When cited the details of both are used in the bibliography. This script looks at a biblatex file and checks that everything with a crossref field has a corresponding entry, and is of a suitable type. You will need to have installed the Python [bibtexparser](https://pypi.python.org/pypi/bibtexparser) package. The '-expand' option modifies the file by copying the information from the referenced entries into those that reference them. A backup is made first.

# convertbibliography.py

This script changes the format of bibliographies to follow (my own opinionated version of) Biblatex style. A backup is made before anything is changed. Most of the heavy lifting is done by [bibtexparser](https://pypi.python.org/pypi/bibtexparser) (see above). You will need to have installed the Python [titlecase](https://pypi.python.org/pypi/titlecase) package. My own additions are extra functions to be used as customizations. Some are left unused because after writing them I decided I didn't want them. As currently written the script will:

* Put authors into last name, first name order (although this will go wrong with multi-word last names) and fix their case
* Put titles in title case
* Convert 'journal' fields to 'journaltitle' for article entries
* Make sure that page ranges use '--' not '-' or '–'
* Remove 'pp.' and 'p.' from page fields
* Protect 'and' in publisher names, which Biblatex would otherwise interpret as a list
* Remove ordinals from editions

# references.py

This script takes a markdown file and biblatex file as arguments. It checks that every reference in the file occurs in the bibliography. If the `--unused` option is given then instead the script checks whether there are items in the bibliography that aren't used in the markdown file.
