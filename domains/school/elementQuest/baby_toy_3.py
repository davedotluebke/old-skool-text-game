import thing

def clone():
    baby_toy_3 = thing.Thing('toy', 'baby bean bag', 'This little been bag is designed to be baby safe. It is part white and part black')
    baby_toy_3.add_adjectives('baby', 'bean', 'little', 'bag', 'white', 'black', 'part', 'and')
    baby_toy_3.add_names('bag')
    baby_toy_3.set_weight(35)
    baby_toy_3.set_volume(0.2)

    return baby_toy_3