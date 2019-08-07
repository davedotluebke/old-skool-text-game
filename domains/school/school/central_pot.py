import container

def clone():
    pot = container.Container('pot', __file__)
    pot.set_description('central pot', 'This pot stands in the centre of the room, over a hot fire.', unlisted=True)
    pot.fix_in_place("You can't move the pot, as it is far to heavy.")
    return pot
