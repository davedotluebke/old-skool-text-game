import thing

def clone():
    scale = thing.Thing('dragon scale', __file__)
    scale.set_description('golden dragon scale', 'This is a golden dragon scale. It is used in many very strong potions.')
    scale.add_adjectives('dragon', 'golden')
    scale.add_names('scale')
    return scale
