import thing

def clone():
    shovel = thing.Thing('shovel', __file__)
    shovel.set_description('shovel', 'This metal shovel is comparitively plain.')
    shovel.add_adjectives('plain', 'metal')
    return shovel
