# crossrefs.py

Biblatex uses a 'crossref' field to link entries together. For example, a chapter in an edited volume will be of type 'incollection' and have a crossref to an entry of type 'collection'. When cited the details of both are used in the bibliography. This script looks at a biblatex file and checks that everything with a crossref field has a corresponding entry, and is of a suitable type. You will need to have installed the Python [bibtexparser](https://pypi.python.org/pypi/bibtexparser) package. The `--expand` option modifies the file by copying the information from the referenced entries into those that reference them. A backup is made first.

# references.py

This script takes a markdown file and biblatex file as arguments. It checks that every reference in the file occurs in the bibliography. If the `--unused` option is given then instead the script checks whether there are items in the bibliography that aren't used in the markdown file.

# fixbibliography.py

The functionality here has been replaced by [github.com/twsh/Convertbibliography](https://github.com/twsh/Convertbibliography).
