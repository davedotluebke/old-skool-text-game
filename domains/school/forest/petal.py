import thing

species = "flower"

def clone():
    petal = thing.Thing('%s petal' % species, __file__)
    petal.set_description('%s petal' % species, 'This is a petal from a %s.' % species)
    petal.add_names('petal')
    petal.add_adjectives(species)
    petal.set_volume(0.0005)
    petal.set_weight(0.5)
    return petal

def set_species(n_species):
    global species
    species = n_species

