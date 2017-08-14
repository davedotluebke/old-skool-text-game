import container

def clone():
    bag = container.Container('bag', __file__)
    bag.set_description('normal bag', 'A normal-looking brown bag.')
    bag.set_weight(100)
    bag.set_volume(10)
    bag.set_max_weight_carried(20000)
    bag.set_max_volume_carried(10)
    bag.closable = True
    return bag