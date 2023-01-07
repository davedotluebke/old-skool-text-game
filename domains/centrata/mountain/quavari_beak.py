import weapon

def clone(): 
    weap = weapon.Weapon("beak", __file__, 4, 5, 1, attack_verbs=["peck", "bite"])
    weap.set_description("beak", "The Quavari's beak is a fearsome weapon.")
    return weap
