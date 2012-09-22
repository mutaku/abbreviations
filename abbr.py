import zipfile
import re
import itertools


class Document():
    '''
    Handles DOCX files for searching abbreviations.
    '''
    def __init__(self, doc, database):
        self.doc = doc
        self.database = database
        self.content = self.parse()
        
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
    
    def parse(self):
        '''
        Parses DOCX XML file for text content.
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
        abbrs = re.compile("\((?P<abb>\d*[a-z]\w*)\)",
                           re.DOTALL|re.IGNORECASE|re.MULTILINE)
        # Get all matches
        # Let's also try to make some singular forms
        chain = itertools.chain(
            *[[x] if not x.endswith('s') else [x, x[:-1]]
                for x in abbrs.findall(self.content)])
        return list(chain)

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
            matches[abbr] = re.findall("^%s.*?\\n" % abbr,
                                    self.content,
                                    re.MULTILINE|re.IGNORECASE)
        return matches