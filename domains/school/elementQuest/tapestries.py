import room
import gametools
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('tapestries', roomPath)
    r.indoor = True
    r.set_description('room with many tapestries hanging', 'This smaller circular room has many tapestries hanging around it.')
    r.add_exit('northwest', 'domains.school.elementQuest.firepit')
    r.add_exit('south', 'domains.school.elementQuest.shaft_of_sunlight')
    
    cloth = gametools.clone('domains.school.elementQuest.cloth')
    r.insert(cloth)

    tapestry1 = scenery.Scenery('tapestry', 'tapestry decorated with dancing flames', 'This tapestry has a fire with dancing flames woven into it. It almost seems as if the fire on it was actually burning.')
    tapestry1.add_response(['take', 'get'], 'You feel as if this tapestry should not be taken...as if you would be taking a piece of the room.')
    tapestry1.add_adjectives('dancing', 'flames')
    r.insert(tapestry1)

    tapestry2 = scenery.Scenery('tapestry', 'tapestry decorated with burning embers', 'This tapestry has the burning embers of a fire woven into it. It almost seems as if they were actual coals.')
    tapestry2.add_response(['take', 'get'], 'You feel as if this tapestry should not be taken...as if you would be taking a piece of the room.')
    tapestry2.add_adjectives('burning', 'embers')
    r.insert(tapestry2)

    return r