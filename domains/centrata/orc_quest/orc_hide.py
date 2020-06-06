import armor

def clone():
    hide = armor.Armor('hide', __file__, 25, 2)
    hide.set_description('hide armor', 'A long tunic made of tough, crudely tanned hide from some large '
        'animal.  Despite its crude construction, wearing it will some protection in a fight.')
    hide.add_adjectives('crude', 'long')
    hide.add_names('hide', 'armor', 'tunic')

    return hide