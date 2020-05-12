import thing

def clone(flower_type):
    petal = thing.Thing('%s petal' % flower_type, __file__)
    petal.set_description('%s petal' % flower_type, 'This is a petal from a %s.' % flower_type)
    petal.add_names('petal')
    petal.add_adjectives(flower_type)
    petal.set_volume(0.0005)
    petal.set_weight(0.5)
    return petal
