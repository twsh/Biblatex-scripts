# crossrefs.py

Biblatex uses a 'crossref' field to link entries together. For example, a chapter in an edited volume will be of type 'incollection' and have a crossref to an entry of type 'collection'. When cited the details of both are used in the bibliography. This script looks at a biblatex file and checks that everything with a crossref field has a corresponding entry, and is of a suitable type. You will need to have installed the Python [bibtexparser](https://pypi.python.org/pypi/bibtexparser) package. The `--expand` option modifies the file by copying the information from the referenced entries into those that reference them. A backup is made first.

# references.py

This script takes a markdown file and biblatex file as arguments. It checks that every reference in the file occurs in the bibliography. If the `--unused` option is given then instead the script checks whether there are items in the bibliography that aren't used in the markdown file.

# fixbibliography.py

This script takes files as arguments. The first is checked for biblatex entries without citekeys. Any that are found are given a dummy cite key. A blank line is added to the beginning of the file if there isn't one already. The result is written to STDOUT. If a second argument is given the output is sent there. Alternatively, the script can read its input from STDIN. The result is a file that [BibDesk](http://bibdesk.sourceforge.net) can open.
