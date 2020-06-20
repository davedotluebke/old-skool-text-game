import armor

def clone():
    leather_suit = armor.Armor('heavy_armor', __file__, 84, 29)
    leather_suit.set_description('heavy armor', 'This is a very strong but extreamly heavy suit of plate armor.')
    leather_suit.add_adjectives('heavy','iron')
    leather_suit.add_names('iron')

    return heavy_armor