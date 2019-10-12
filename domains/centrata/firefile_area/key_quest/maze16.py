import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage, with a giant peice of cave bacon on the celling.')
    r.add_exit('south', 'domains.centrata.firefile_area.key_quest.maze28')
    r.add_exit('west', 'domains.centrata.firefile_area.key_quest.maze47')

    cave_bacon = scenery.Scenery ('cave bacon', 'strip of cave bacon', 'This is cave bacon looks like a larger than life strip of bacon, super large and cripy, YUM!')
    cave_bacon.add_response(['take'], 'You try to take the cave bacon, but it is fastened to the ceiling;.')
    cave_bacon.add_response(['eat'], 'The cave bacon is far too hard to eat.')
    cave_bacon.unlisted = True
    r.insert(cave_bacon, True)

    return r
