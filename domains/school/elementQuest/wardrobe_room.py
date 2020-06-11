import room
import gametools
import scenery


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('room', roomPath, indoor=True)
    r.set_description('wardrobe room', 'You find yourself in a small room with a large wardrobe against one wall. There is a small doorway to the west.')
    r.add_adjectives('wardrobe')
    r.add_exit('west', 'domains.school.elementQuest.statue_room')

    wardrobe = gametools.clone('domains.school.elementQuest.wardrobe')
    r.insert(wardrobe)
    
    return r
