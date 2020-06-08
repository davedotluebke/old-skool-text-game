import thing

def clone():
    truffles = thing.Thing('truffles', __file__)
    truffles.set_description('truffles', 'These truffles look very determined for some reason.')
    return truffles