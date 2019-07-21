import potions

def clone():
    i = potions.InvisibilityPotion('invisibility potion', __file__, 'invisibility potion', 'This is an invisibility potion. It seems almost clear, but it seems you can\'t quite look at it.')
    i.add_names('potion')
    i.add_adjectives('invisibility')
    return i