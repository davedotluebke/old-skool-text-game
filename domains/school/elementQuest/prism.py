import thing

def clone():
    prism = thing.Thing('prism', __file__)
    prism.set_description('large triangular prism', 'This is a large traingular prism. It seems to be very delicately cut.')
    prism.add_adjectives('large', 'delicate', 'triangular')
    return prism
