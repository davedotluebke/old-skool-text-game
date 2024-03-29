import gametools
import scenery
import room
from domains.centrata.mansion.safe_door import SafeDoorOutside

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('office', roomPath, indoor=True)
    r.set_description('mahogany-panelled office', 'You find yourself in a mahogany-panelled office with books surrounding you on every side. A small desk with fancy carvings stands in the centre of the room. To the east, a large bay window looks out over the lawn. To the west there is a sturdy door to a safe. There is a doorway to the north.')
    r.add_exit('north', 'domains.centrata.mansion.parlour')
    
    safe_door = SafeDoorOutside()
    r.insert(safe_door)

    office_bookcase = gametools.clone('domains.centrata.mansion.office_bookshelf')
    r.insert(office_bookcase, True)

    office_desk = gametools.clone('domains.centrata.mansion.office_desk')
    r.insert(office_desk, True)

    # scenery of office_desk
    desk_fruit_carving_scenery = scenery.Scenery('carving', 'desk fruit carvings', 'These carvings of fruits appear to depict a bountiful supply, with a special focus on pomegranates.', unlisted=True)
    desk_fruit_carving_scenery.add_adjectives('desk', 'fruit', 'pomegranates')
    desk_fruit_carving_scenery.add_names('fruit')
    r.insert(desk_fruit_carving_scenery, True)

    return r
