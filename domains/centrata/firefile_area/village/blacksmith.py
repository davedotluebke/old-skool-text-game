import shop
import gametools

def clone():
    smith = shop.Shopkeeper('blacksmith', __file__, None)
    smith.set_description('grizzled blacksmith', 'This grizzled old blacksmith looks as if he has worked '
        'behind this forge for a hundred years.')
    smith.set_default_items(gametools.clone('domains.centrata.firefile_area.village.hook'))

    return smith
