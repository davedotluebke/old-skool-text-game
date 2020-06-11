import thing

def clone():
    spring = thing.Thing('spring', __file__)
    spring.set_description('rusty spring', 'This spring is old and rusty. It seems to still have energy, though.')
    spring.add_adjectives('old', 'rusty')
    return spring
