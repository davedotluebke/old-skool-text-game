import weapon

def clone(): 
    weap = weapon.Weapon("bare hands", __file__, 1, 5, 1, attack_verbs=["hit"])
    weap.set_description("bare hands", "your bare hands")
    return weap