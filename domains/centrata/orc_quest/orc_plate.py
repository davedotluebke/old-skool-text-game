import armor

def clone():
    plate = armor.Armor('armor', __file__, 40, 3)
    plate.set_description('plate armor', 'A set of sculpted iron plates '
        'held on by leather straps, this armor is incredibly heavy but will '
        'deflect all but the mightiest blows. It stinks of orc.')
    plate.set_weight(35000)
    plate.add_adjectives('plate', 'iron', 'sculpted')
    plate.add_names('plate', 'plates')

    return plate