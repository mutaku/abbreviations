Find scientific abbreviations

Currently, parses DOCX files and searches for abbreviations in the 
format of (abbreviation). These are then searched against a list of
programatically generated MEDLINE abbreviations and supplies all 
possible matches for further selection.

ADAM is used for the MEDLINE database list.
More can be found here: [ADAM: Another Database of Abbreviations in MEDLINE](http://arrowsmith.psych.uic.edu/arrowsmith_uic/adam.html)

Usage:

```Python
from abbreviations import abbr

# Initiate manuscript
doc = abbr.Document("location/of/manuscript.docx",
        "location/of/adam_database".
        "adam")

# Load up our database
doc.import_database()

# Get a dictionary of results
all_results = doc.search_database()

# All our abbreviations
all_results.keys()

# Iterate over matches in MEDLINE database for an abbreviation
for match in all_results['DMSO'].items():
    print match

# Suck out only specific parsed data from results
for k, match in all_results['DMSO'].items():
    print "abbr: %s -> %s" % (match['abbr'], match['def'])

# Grab the top result from an abbreviation match
top_dmso = doc.get_top(all_results['DMSO'])

# Definition of the top result
top_dmso['def']

```
