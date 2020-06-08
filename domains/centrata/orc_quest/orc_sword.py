import weapon

def clone():
    sword = weapon.Weapon('sword', __file__, 10, 30, 2, attack_verbs=["swing","hit"])
    sword.set_description('orc sword', "This sword is simple but well-made, clearly fashioned by "
        "human or even dwarvish smiths.  Crude orc-runes have been scratched into the metal, "
        "probably with a rock, testifying to the cruel end met by its unfortunate former owner. "
        "Despite a strong smell of orc, the sword is well balanced and sharp."

    return sword