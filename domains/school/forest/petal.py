import thing

def clone():
    petal = thing.Thing('sunflower petal', __file__)
    petal.set_description('sunflower petal', 'This is a petal from a sunflower.')
    petal.add_names('petal')
    petal.add_adjectives('sunflower')
    return petal