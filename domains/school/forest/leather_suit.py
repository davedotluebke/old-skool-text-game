import armor

def clone():
    leather_suit = armor.Armor('leather_suit', __file__, 25, 2)
    leather_suit.set_description('leather suit', 'A crude tunic made of sturdy leather hide. Wearing it should provide some protection in a fight.')
    leather_suit.add_adjectives('leather')
    leather_suit.add_names('hide','suit')

    return leather_suits