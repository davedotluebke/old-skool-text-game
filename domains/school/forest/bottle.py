import container

def clone():
        
    bottle = container.Container('bottle', __file__)
    bottle.set_description('blue bottle', 'This blue bottle looks like a normal plastic bottle. It is unlabeled.')
    bottle.add_adjectives('blue', 'plastic', 'unlabeled')
    bottle.set_max_weight_carried(4e9)
    bottle.set_max_volume_carried(3e9)
    bottle.liquid = True

    return bottle
