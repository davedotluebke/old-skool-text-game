import container
import gametools

def clone():
    shelving = container.Container('shelving', __file__)
    shelving.set_description('wooden shelving', 'This rotting wooden shelving is fastened to the walls.')
    shelving.add_adjectives('wooden', 'rotting', 'cellar')
    shelving.fix_in_place("The shelving has been fixed to the wall for too long to be moved without destroying it.")
    shelving.set_prepositions('on', 'onto')
    shelving.set_max_volume_carried(1000)
    shelving.set_max_weight_carried(5000)

    rope = gametools.clone('domains.centrata.mountain.rope')
    shelving.insert(rope, True)
    
    return shelving
