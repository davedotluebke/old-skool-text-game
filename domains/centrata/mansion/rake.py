import thing

def clone():
    rake = thing.Thing('rake', __file__)
    rake.set_description('rake', 'This rake is made of a wooden handle with red tines.')
    rake.add_adjectives('red')
    return rake
