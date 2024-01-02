import thing

def clone():
    teddy_bear = thing.Thing('bear', __file__)
    teddy_bear.set_description('teddy bear', 'This is a brown teddy bear.')
    teddy_bear.add_adjectives('teddy', 'brown')
    teddy_bear.set_flammable(5)
    teddy_bear.set_weight(500)
    teddy_bear.set_volume(1.5)
    teddy_bear.set_value(5)
    return teddy_bear
