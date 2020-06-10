import money

def clone():
    gold = money.Money('gold', __file__, value=400)
    gold.set_description('gold coin', 'This is a shiny gold coin.')
    gold.add_names('coin')
    gold.add_plural_names('coins')
    gold.add_adjectives('gold', 'shiny')
    return gold
