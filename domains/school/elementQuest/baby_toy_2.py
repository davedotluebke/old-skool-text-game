import thing

def clone():
    baby_toy_2 = thing.Thing('toy', 'baby ball', 'This is a little squishy ball designed for babys to play with. It is striped in purple, orange and yellow.')
    baby_toy_2.add_adjectives('baby', 'ball', 'little', 'purple', 'orange', 'yellow', 'striped', 'squishhy')
    baby_toy_2.add_names('ball')
    baby_toy_2.set_weight(25)
    baby_toy_2.set_volume(0.05)

    return baby_toy_2