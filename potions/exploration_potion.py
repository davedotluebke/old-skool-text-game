import potions

def clone():
    i = potions.ExplorationPotion('exploration potion', __file__, 'exploration potion', 'This exporation potion feels magnetic, almost as if it wanted to pull you to somewhere else.')
    i.add_names('potion')
    i.add_adjectives('exploration')
    return i
