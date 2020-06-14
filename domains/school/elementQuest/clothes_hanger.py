import thing

def clone():
    hanger = thing.Thing('hanger', __file__)
    hanger.set_description('clothes hanger', 'This is a hanger used to hang clothing.')
    hanger.add_adjectives('clothes', 'clothing')
    return hanger
