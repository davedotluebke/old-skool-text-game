import container
import gametools

def clone():
    ice_chest = container.Container('chest', __file__)
    ice_chest.set_description('ice chest', 'This is a fancy mahogany ice chest. Its panels a intricately carved to resemble various types of birds in flight.')
    ice_chest.add_names('cooler', 'box')
    ice_chest.add_adjectives('ice', 'cooler', 'cooling', 'cold')
    ice_chest.closable = True

    ice_block = gametools.clone('domains.school.elementQuest.ice_block')
    ice_block.plurality = 5

    ice_chest.closable = True
    ice_chest.set_max_volume_carried(100)
    ice_chest.set_max_weight_carried(50000)
    ice_chest.fix_in_place('The ice chest is held firerly to the floor so you can\'t move it.')

    ice_chest.insert(ice_block)
    ice_chest.close()

    return ice_chest
