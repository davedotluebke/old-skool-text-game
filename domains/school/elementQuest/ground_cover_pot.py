import thing

def clone():
    ground_cover_pot = thing.Thing('pot', __file__)
    ground_cover_pot.set_description('ground cover pot', 'This small pot is over-flowing with english ivy.', 'ground cover pots')
    ground_cover_pot.add_adjectives('ivy', 'english', 'small', 'over-flowing')
    ground_cover_pot.set_weight(1300)
    ground_cover_pot.set_volume(3)

    return ground_cover_pot