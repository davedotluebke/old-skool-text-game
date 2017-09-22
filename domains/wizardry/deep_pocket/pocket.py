import domains.wizardry.deep_pocket.classes as classes

def clone():
    new_pocket = classes.DeepPocket('pocket', classes.DeepPocket.vault_room, classes.DeepPocket.customer, __file__)
    new_pocket.set_description('deep pocket', 'This is a magical deep pocket. Putting things in the pocket transports them to an infinite space vault.')
    return new_pocket
