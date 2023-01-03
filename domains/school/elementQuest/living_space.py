import room
import gametools
import scenery
import doors_and_windows

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('room', roomPath, indoor=True)
    r.set_description('living room', 'This is a small, comfortable living room.'
    ' There is a leather couch in the middle of the room. Above the couch there is '
    'a large painting of a bird. You see a door to the west, a door to the east, '
    'and a staircase along one wall leads up and down.')
    r.add_adjectives('living')
    r.add_exit('up', 'domains.school.elementQuest.lookout')
    r.add_exit('down', 'domains.school.elementQuest.armor_museum')

    west_door = doors_and_windows.Door('door', 'wooden door', 'This is a wooden door on the west side of the room.', 'domains.school.elementQuest.study', 'west', [])
    west_door.add_adjectives('wooden')
    r.insert(west_door)

    east_door = doors_and_windows.Door('door', 'wooden door', 'This is a wooden door on the east side of the room.', 'domains.school.elementQuest.nursury', 'east', [])
    east_door.add_adjectives('wooden')
    r.insert(east_door)

    couch = gametools.clone('home.johanna.house.couch')
    r.insert(couch)

    painting = scenery.Scenery('painting', 'painting of a bird', 'This is a painting of a bird. It is in an impressionistic style. You cannot tell what type of bird it is.')
    painting.add_adjectives('bird', 'impressionistic', 'style')
    painting.add_response(['take','steal','get'], 'You decide not to take the painting, as it belongs to someone else.')
    r.insert(painting)

    return r
    