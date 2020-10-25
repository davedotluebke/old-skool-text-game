import weapon

def clone():
    scimitar = weapon.Weapon('scimitar', __file__, 30, 25, 3, attack_verbs=["swing","hit"])
    scimitar.set_description('orc scimitar', "The wicked curve of this exotic weapon "
        "bespeaks an almost elegant brutality.  The blade gleams with an almost unnaturally "
        "sharp edge, and the metal has somehow been imbued with a swirling pattern that "
        "seems almost to flow as you gaze upon it.  This scimitar is clearly the product "
        "of elvish smiths from the east, but has been defiled by orc-runes along the length "
        "of the huge blade. It smells strongly of orc.")

    return scimitar