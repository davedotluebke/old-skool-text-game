import weapon

def clone():
    sword = weapon.Weapon('sword', __file__, 6, 30, 2, attack_verbs=["swing","stab","thrust"])
    sword.set_description('rusty old sword', "This is a rusty old sword. It's not very sharp but is still better than bare hands.")

    return sword