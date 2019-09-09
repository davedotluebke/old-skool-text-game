import potions

def clone():
    i = potions.PinkPotion('pink potion', __file__, 'pink potion', 'This is an pink potion. It is hot pink, and makes anyone that drinks it hot pink too.')
    i.add_names('potion')
    i.add_adjectives('pink')
    return i