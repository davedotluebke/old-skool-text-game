import weapon

def clone():
    knife = weapon.Weapon('knife', __file__, 10, 30, .5)
    knife.set_description('small knife', 'This is a small single edged knife. The blade gleems in the sun.')
    knife.add_adjectives('sharp''small')
    return knife
