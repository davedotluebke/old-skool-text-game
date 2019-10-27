import container

def clone():
    pot = container.Container('oven', __file__)
    pot.set_description('clay oven', 'This clay oven is set into the wall, and is very hot.', unlisted=True)
    pot.fix_in_place("The clay oven is set into the wall.")
    return pot
