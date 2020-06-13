import armor

def clone():
    leather_suit = armor.Armor('leather_suit', __file__, 37, 1.5)
    leather_suit.set_description('warm leather suit', 'This leather suit consists of: boots, pants, a tunic, and a cap, made of very sturdy leather. It looks like it provides a lot of warmth and protection.')
    leather_suit.add_adjectives('leather', 'strong')
    leather_suit.add_names('suit')

    return leather_suit     