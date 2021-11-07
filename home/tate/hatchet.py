import weapon

def clone():
    hatchet = weapon.Weapon('hatchet', __file__, 14, 16, 2)
    hatchet.set_description('small hatchet', 'This small hatchet has a nice mahogany handle, the rest is stainless steel.')
    hatchet.add_adjectives('small', 'powerful')
    
    return hatchet
