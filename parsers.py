# Parsers specific to various abbreviations databases

def adam(abbr):
    '''
    Parses provided match and restructures
    matches by ADAM database format.
    '''
    # Format for ADAM (tab delimited):
    #  Standard abbreviation
    #  Other abbreviations
    #  Long forms (definitions) and score
    #  Score (likelihood of phrase)
    #  Count (usage occurences)
    results = dict()
    # Enumerate over list of matches for a
    # given abbreviation (abbr)
    for k, entry in enumerate(abbr):
        # Entries are tab delimited
        match = entry.split("\t")
        results[k] = {
            'abbr': match[0],
            'other_abbr': match[1],
            'def': match[2],
            'score': match[3],
            'count': match[4]}
    return results