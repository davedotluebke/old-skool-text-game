import thing

def clone():
    hoe = thing.Thing('hoe', __file__)
    hoe.set_description('wood-handled hoe', 'This wood-handled hoe has a metal end.')
    hoe.add_adjectives('wood-handled')
    return hoe
