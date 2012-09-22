import zipfile
import re
import itertools
from tools import plurals
import parsers

class Document():
    '''
    Handles DOCX files for searching abbreviations.
    Parses doc_file to find abbreviations used and then
    looks up long form/definition in given database file.
    '''
    def __init__(self, doc_file, db_file, db_type="adam"):
        self.doc = doc_file
        self.database = db_file
        self.db_type = db_type # defaults to ADAM
        self.content = self.read()
        
        # Setup database-specific parsing
        # As additional database are used we can add
        # them here and no other code needs changed
        self.parsers = {
            "adam": parsers.adam,}
        
    def opener(self):
        '''
        Opens DOCX XML file.
        '''
        # Unzip DOCX and return the xml file
        file_obj = zipfile.ZipFile(self.doc)
        return file_obj.read('word/document.xml')
    
    def cleanup(self, data):
        '''
        Substitutes garbage chars for a whitespace.
        '''
        # Sub out XML junk
        return re.sub("<(.|\n)*?>", " ", data)
    
    def read(self):
        '''
        Reads DOCX XML file for text content.
        '''
        # Get XML content and pass through the cleaner
        xml_content = self.opener()
        return self.cleanup(xml_content)

    def find_abbr(self):
        '''
        Finds abbreviations in data like (abbr).
        '''
        # Find (abbr) structured items
        # Ignore only digits as they are references
        # We pull out only the internal text 'abbr' of (abbr)
        abbrs = re.compile("\((?P<abb>\d*[a-z]\w*)\)",
                           re.DOTALL|re.IGNORECASE|re.MULTILINE)
        # Get all matches
        # Run results through plurals tool to try and
        # get possible singular forms of an abbreviation
        # Use itertools.chain to flatten out nested lists
        chain = itertools.chain(
            *[plurals(x) for x in abbrs.findall(self.content)])
        # Pass through set to remove duplicates
        return list(set(chain))

    def import_database(self):
        '''
        Imports the provided abbreviations database file.
        '''
        # We just read this into an object we can later parse
        # Need to make sure we use multiline with regex since
        # we are not splitting lines like we would with readlines()
        self.abbreviations = open(self.database, "r").read()

    def search_database(self):
        '''
        Builds dictionary of potential abbreviation definitions
        by searching database file for parsed abbreviations in
        content file.
        '''
        # Builds "abbreviation": [list of potential entries]
        # We can later iterate over each abbreviations possible
        # entries and provide them to the user to select from
        # Current search looks for minimum start:
        # GEF would match GEF and GEFS and so on
        matches = dict()
        for abbr in self.find_abbr():
            # Return the entire line starting with abbr
            # and ending at the newline character
            # This is our custom "grep"
            results = re.findall("^%s.*?\\n" % abbr,
                                    self.abbreviations,
                                    re.MULTILINE|re.IGNORECASE)
            # Pass results through database-specific parser
            # This will be a list of dictionaries since we
            # sort the results based on score before returning
            matches[abbr] = self.parsers[self.db_type](results)
        return matches