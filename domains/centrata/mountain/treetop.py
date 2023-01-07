import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    treetop = room.Room('treetop', roomPath)
    treetop.set_description('high treetop', 'This high tretop overlooks the entire mountain. From here you can see a hut atop the mountain, a mountain range to the west, a village to the north, and a prairie to the east. Strangely, you see smoke rising from the middle of the prairie.')
    treetop.add_exit('down', 'domains.centrata.mountain.woods')

    nest = gametools.clone('domains.centrata.mountain.nest')
    treetop.insert(nest, True)

    quavari = gametools.clone('domains.centrata.mountain.quavari')
    treetop.insert(quavari, True)
    nest.contents[0].quavari = quavari # used for making the quavari attack
    
    return treetop
