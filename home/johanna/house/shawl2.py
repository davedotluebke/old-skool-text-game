import thing

def clone():
    shawl = thing.Thing('shawl', __file__)
    shawl.set_description('bright orange shawl', 'This bright orange shawl is very clean and soft.')
    shawl.set_weight(200)
    shawl.set_volume(0.1)
    return shawl
