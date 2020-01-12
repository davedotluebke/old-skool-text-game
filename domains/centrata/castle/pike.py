import weapon

def clone():
    pike = weapon.Weapon('pike', __file__, 10, 20, 3, attack_verbs=["stab", "pierce"])
    pike.set_description('ancient pike', 'This once finely made pike has corroded over the ages but is still a formidable weapon.')

    return pike