import money

def clone():
    copper = money.Money('copper', __file__, value=1)
    copper.set_description('copper coin', 'This is a shiny copper coin.')
    copper.add_names('coin')
    copper.add_plural_names('coins')
    copper.add_adjectives('copper', 'shiny')
    return copper
