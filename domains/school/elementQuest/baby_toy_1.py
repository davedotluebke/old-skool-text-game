import thing

def clone():
    baby_toy_1 = thing.Thing('toy', __file__)
    baby_toy_1.set_description('baby rattle', 'This is a little baby rattle. It is painted in red, green and blue.')
    baby_toy_1.add_adjectives('baby', 'rattle', 'little', 'red', 'green', 'blue', 'painted')
    baby_toy_1.add_names('rattle')
    baby_toy_1.set_weight(70)
    baby_toy_1.set_volume(0.07)

    return baby_toy_1