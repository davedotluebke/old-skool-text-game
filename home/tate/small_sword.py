import weapon

def clone():
    sword = weapon.Weapon('knife', __file__, 14, 17, 1.5)
    sword.set_description('small sword', 'This is a small sword, made out of steel. The blade gleems in the sun.')
    sword.add_adjectives('sharp')
    return sword
