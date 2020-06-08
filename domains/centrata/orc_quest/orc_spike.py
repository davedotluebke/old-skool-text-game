import weapon

def clone():
    spike = weapon.Weapon('spike', __file__, 5, 20, 4, attack_verbs=["stab","hit"])
    spike.set_description('spike', "This long metal spike makes a crude but effective weapon
        "that you can stab at your opponent. It smells of orc.")

    return spike