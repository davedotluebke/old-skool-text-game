import container

def clone():    
    cup = container.Container('cup', __file__)
    cup.set_description('ceramic cup', 'This is an ordinary ceramic cup. It has no decorations.')
    cup.add_adjectives('ceramic', 'undecorated')
    cup.set_max_weight_carried(400000)
    cup.set_max_volume_carried(3)
    cup.liquid = True

    return cup
