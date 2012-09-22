# Extra tools

def plurals(element):
    '''
    Attempts to return element and it's singular
    form if plural.
    '''
    # This will evolve but starting basic
    # We want to return a list that contains
    # original element and singular form if we
    # think we have a plural abbreviation
    # For now, we do a simple check:
    # is our element like GEFs?
    # If so, return GEFs and GEF.
    # In essence, we assume that pluralization
    # will be lower case and the abbr root upper
    # We do not use list comprehension so we can
    # more explicitly handle looking for plurals
    # and expand our algorithm
    abbrs = [element]
    # Start with the more inclusive first
    if element.endswith('es'):
        abbrs.append(element[:-2])
    # Then look for simpler forms
    elif element.endswith('s'):
        abbrs.append(element[:-1])
    return abbrs
    