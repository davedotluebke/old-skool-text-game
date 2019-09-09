import weapon

def clone():
    bite = weapon.Weapon('bite', __file__, 1, 34, 1)
    bite.set_description('strong bite', 'This bite feels strong.')
    return bite