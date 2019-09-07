import potions

def clone():
    i = potions.PinkPotion('strength potion', __file__, 'strength potion', 'This is an strength potion. You can almost see the energy bubling up in it.')
    i.add_names('potion')
    i.add_adjectives('strength')
    return i