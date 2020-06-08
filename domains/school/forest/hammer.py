import weapon

def clone():
    hammer = weapon.Weapon('hammer', __file__, 6, 20, 4, attack_verbs=["hit","swing","pound"])
    hammer.set_description('large hammer', 'This large iron hammer would be a formidable weapon, if a little unwieldy.')
    hammer.add_adjectives('large', 'unwieldy', 'formidable', 'iron')
    return hammer
