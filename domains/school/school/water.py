import liquid

def clone():
    water = liquid.Liquid('water', __file__, 'normal water', 'This is some normal, clear water.')
    water.path = 'domains.school.school.water'
    water.add_response(['drink'], 'You take a big drink of the water, and your thirst is quenched.')
    return water
