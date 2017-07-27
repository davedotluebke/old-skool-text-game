import thing

def clone(): 
    plate = thing.Thing('plate', __file__)
    plate.set_description('dinner plate', 'This is a normal-looking white dinner plate.')
    plate.set_weight(1000)
    plate.set_volume(1.25)
    plate.add_adjectives('dinner','white')

    return plate