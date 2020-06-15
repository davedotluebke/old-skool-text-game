import weapon

def clone():
    knife = weapon.Weapon('sword', __file__, 14, 17, 1.5)
    knife.set_description('small sword', 'This is a small sword, made out of steel. The blade gleems in the sun.')
    knife.add_adjectives('sharp')
    return knife
