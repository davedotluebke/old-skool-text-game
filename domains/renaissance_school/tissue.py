import thing

def clone():
    tissue = thing.Thing('kleenex', __file__)
    tissue.set_description('thin kleenex', 'This is a very thin kleenex.')
    tissue.add_adjectives('thin')
    tissue.add_names('tissue')
    return tissue
