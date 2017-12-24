import thing

def clone():
    gold = thing.Thing('gold', __file__)
    gold.set_description('bunch of shiny gold coins', 'This is a collection of seven shiny, real gold coins.')
    gold.set_weight(74000)
    return gold
