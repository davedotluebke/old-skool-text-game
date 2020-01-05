import weapon

def clone():
    club = weapon.Weapon('club', __file__, 5, 20, 4, attack_verbs=["swing","hit"])
    club.set_description('crude club', "This crude club is simply a heavy tree branch fashioned into a "
        "clumsy but effective club by driving some sharp rocks and nails into the business end. It "
        "smells of orc."

    return club