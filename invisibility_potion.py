import potions

def clone():
    i = potions.InvisibilityPotion('invisibility potion', 'invisibility potion', 'This is an invisibility potion.')
    i.add_names('potion')
    i.add_adjectives('invisibility')
    return i