import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('field', roomPath)
    r.set_description('bright field', 'You slowly step into a bright field, filled with waving grass. There is a scroll on the ground.')
    
    scroll = gametools.clone('domains.centrata.firefile_area.key_quest.scroll1')
    scroll.move_to(r)

    hay = gametools.clone('domains.centrata.firefile_area.key_quest.hay')
    hay.move_to(r)

    r.add_exit('east', 'domains.centrata.firefile_area.fields.road_eight')
    return r
