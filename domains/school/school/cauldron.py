import gametools
import cauldron

def clone():
    n_cauldron = cauldron.Cauldron('cauldron', __file__)
    n_cauldron.set_description('iron cauldron', 'This is an iron cauldron.')
    n_cauldron.set_max_weight_carried(2000)
    n_cauldron.set_max_volume_carried(30)
    return n_cauldron