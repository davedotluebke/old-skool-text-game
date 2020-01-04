import weapon

def clone():
    hook = weapon.Weapon('hook', __file__, 3, 20, 4, attack_verbs=["swing","stab","thrust"])
    hook.set_description("farmer's thatching hook", "This heavy iron farm implement is used for "
        "thatching hay, but can be used as a weapon in a pinch - swing, stab, or thrust it at your "
        "opponent.")

    return hook