import weapon

def clone(): 
    weap = weapon.Weapon("claws", __file__, 4, 5, 1, attack_verbs=["scratch"])
    weap.set_description("claws", "The Quavari's claws are a fearsome weapon.")
    return weap
