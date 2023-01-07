import container
import gametools

def clone():
    nest = container.Container('nest', __file__)
    nest.set_description('alpine nest', 'This alpine nest is nestled in the tops of the highest pine tree.')
    nest.add_adjectives('alpine')
    nest.fix_in_place('You cannot take this nest without breaking it.')

    key = gametools.clone('domains.centrata.mountain.key')
    nest.insert(key, True)
    
    return nest
