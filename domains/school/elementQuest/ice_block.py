import thing

def clone():
    ice_block = thing.Thing('block', __file__)
    ice_block.set_description('ice block', 'This ice block is large and cold, you wounder what its use is.')
    ice_block.add_adjectives('ice', 'cold', 'large')
    ice_block.add_names('cube', 'ice')
    ice_block.set_weight(1838)
    ice_block.set_volume(2)

    return ice_block