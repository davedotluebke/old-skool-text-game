import thing

def clone():
    scarf = Thing('scarf', __file__)
    scarf.set_description('bright pink scarf', 'This bright pink scarf is very clean and soft.')
    scarf.set_weight(200)
    scarf.set_volume(0.1)
    return scarf
