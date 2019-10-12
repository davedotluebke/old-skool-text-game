import weapon

def clone():
    axe = weapon.Weapon('axe', __file__, 20, 10, 9)
    axe.set_description('large axe', 'This large axe is made of iron. It could form a very powerful weapon if it could be accurately aimed.')
    axe.add_adjectives('large', 'powerful')
    return axe
