import creature

def clone():
    fish = creature.NPC('fish', __file__)
    fish.set_description('red-orange fish', 'This brightly coloured fish is a red-orange. It is also quite large.')
    fish.add_adjectives('red-orange', 'bright', 'large')
    return fish
