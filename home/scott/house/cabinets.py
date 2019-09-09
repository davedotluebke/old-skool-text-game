import container

def clone():
    cabnet = container.Container('cabinet', __file__)
    cabnet.set_description('small cabinet', 'This is a small cabinet above the sink.')
    cabnet.add_adjectives('small')
    cabnet.close()
    cabnet.closable = True
    cabnet.set_max_volume_carried(20)
    cabnet.set_max_weight_carried(1000000)
    return cabnet
