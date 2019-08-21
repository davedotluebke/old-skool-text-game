import money

def clone():
    silver = money.Money('silver', __file__, value=20)
    silver.set_description('silver coin', 'This is a tarnished silver coin.')
    silver.add_names('coin')
    silver.add_adjectives('silver', 'tarnished')
    return silver
