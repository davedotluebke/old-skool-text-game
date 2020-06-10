import room
import gametools
import scenery


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('closet', roomPath, indoor=True)
    r.set_description('china closet', 'You find yourself in a small china closet, where an impressive collection of china is stored in a large glass case. A small doorway leads to the east.')
    r.add_adjectives('china')
    r.add_exit('east', 'domains.school.elementQuest.statue_room')

    glass_case = scenery.Scenery('case', 'glass case', 'This is a large glass case that is built into the room. It holds the large collection of china.', unlisted=True)
    glass_case.add_adjectives('glass', 'large', 'tall')
    glass_case.add_response(['take', 'get'], 'The glass case is built into the room.')
    glass_case.add_response(['open'], 'The case is locked.')
    glass_case.add_response(['unlock'], 'You don\'t have the key.')
    glass_case.add_response(['break', 'destroy', 'force'], 'Despite your best effort, you cannot break the glass case.')
    glass_case.add_response(['close', 'shut'], 'The case is already closed!')
    r.insert(glass_case)

    china_dishes = scenery.Scenery('china', 'fancy china', 'These china dishes have been delicately hand-painted with patterns of birds. You notice a gold rim around the sides.')
    china_dishes.add_names('dishes')
    china_dishes.add_adjectives('fancy', 'hand-painted')
    china_dishes.add_response(['take', 'get'], 'The dishes are stored behind a glass case.')
    r.insert(china_dishes)
    return r
