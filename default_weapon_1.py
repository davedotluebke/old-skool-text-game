import weapon

def clone(): 
    weap = weapon.Weapon("feet", __file__, 1, 5, 1, attack_verbs=["kick"])
    weap.set_description("feet", "your feet")
    return weap