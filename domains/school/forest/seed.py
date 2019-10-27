import thing

def clone():
    seed = thing.Thing('poppyseed', __file__)
    seed.set_description(seed.names[0], 'This is a normal poppy seed.')
    return seed
