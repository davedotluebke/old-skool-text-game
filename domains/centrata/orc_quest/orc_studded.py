import armor

def clone():
    studded = armor.Armor('armor', __file__, 25, 2)
    studded.set_description('studded leather armor', 'A boiled leather tunic and leggings covered with metal '
        'studs, this armor is heavy but effective.')
    studded.add_adjectives('studded', 'leather')
    studded.add_names('tunic', 'leggings')

    return studded