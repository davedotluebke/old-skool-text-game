import container
import gametools
import scenery

def clone():
    ice_melter = container.Container('melter', __file__)
    ice_melter.fix_in_place('You try as hard as you can but you just can\'t budge the ice melter.')
    ice_melter.add_adjectives('hot', 'ice', 'small', 'normal')
    ice_melter.set_description('ice maker', 'This is a small but normal ice melter. It is hot.')