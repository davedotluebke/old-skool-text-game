import potions

def clone():
    i = potions.JumpingPotion('jumping potion', __file__, 'jumping potion', 'This jumping potion is bubbiling merrily. It seems to be constantly moving about.')
    i.add_names('potion')
    i.add_adjectives('jumping')
    return i
