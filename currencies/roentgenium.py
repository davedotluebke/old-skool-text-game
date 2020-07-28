import money

def clone():
    roentgenium = money.Money('roentgenium', __file__, value=8000)
    roentgenium.set_description('roentgenium coin', 'This is a radioactive roentgenium coin.')
    roentgenium.add_names('coin')
    roentgenium.add_plural_names('coins')
    roentgenium.add_adjectives('roentgenium', 'radioactive')
    return roentgenium
