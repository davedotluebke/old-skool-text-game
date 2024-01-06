import thing

def clone():
    ladder = thing.Thing('ladder', __file__)
    ladder.set_description('sturdy ladder', 'This sturdy ladder is made of steel.')
    ladder.add_adjectives('sturdy', 'steel')
    return ladder
