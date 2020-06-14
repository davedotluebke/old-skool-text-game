import weapon

def clone():
    knife = weapon.Weapon('knife', __file__, 8, 20, 1)
    knife.set_description('sharp knife', 'This is a double-edged knife. The blade shimmers very slightly.')
    knife.add_adjectives('sharp', 'double-edged')
    return knife
