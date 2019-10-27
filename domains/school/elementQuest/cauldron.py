import cauldron
import gametools 
        
def clone():
    c = cauldron.Cauldron('cauldron', __file__)
    c.set_description('enormous iron cauldron', 'This is an enormous iron cauldron filled to the brim with a luminous red potion.', unlisted=True)
    c.fix_in_place('This enormous cauldorn is way too heavy to move.')
    c.add_adjectives('enormous', 'iron')

    liquid_fire = gametools.clone('domains.school.elementQuest.liquid_fire')
    c.insert(liquid_fire)
    return c