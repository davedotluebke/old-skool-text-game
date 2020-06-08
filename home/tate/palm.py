import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room("palm", roomPath, indoor=True,safe=True)
    r.set_description('statue', 'You see a golden statue of a palm in front of you. You also see two doors, One to your west and one to your east. the walls are also light blue. it is a very tall room, it also has a big gold dome it has a ladder up it.')
    r.add_adjectives('tall', 'big')
    r.add_exit('south', 'home.tate.entryway')

    palm = scenery.Scenery ('palm', 'statue', 'This beautiful golden statue of a life-size palm tree reminds you of a warm day at the beach.')
    palm.add_response(['clinb'], 'it is slipery,and you cant reech the leaves.')
    r.insert(palm, True
    dome = scenery.Scenery('palm', 'dome', 'the gold dome has a ladder up it, up there, there must be great views!














































































    
    