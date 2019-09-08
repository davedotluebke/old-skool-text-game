import room
import gametools
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    arena = room.Room('arena', roomPath, indoor=True)
    arena.set_description('small arena', 'You look up to find yourself inside a small arena of some sort, with seating facing inwards towards a large central platform. At the top of the steps there are doors to the northeast, the south, and the west.')
    arena.add_adjectives('small')
    arena.add_exit('northeast', 'domains.school.school.library')
    arena.add_exit('south', 'domains.school.school.balcony')
    arena.add_exit('west', 'domains.school.school.four_worlds_room')

    platform = scenery.Scenery('platform', 'small platform', 'This small platform is undecorated. It stands slightly higher than than the lowest seating.')
    platform.add_adjectives('small', 'high')
    platform.add_response(['stand', 'mount'], 'You stand on the platform, feeling more confident than before.')
    platform.move_to(arena, True)

    seating = scenery.Scenery('seating', 'seating', 'This seating overlooks the platform in the middle of the room.')
    seating.add_response(['sit'], 'You sit in one of the seats.')
    seating.move_to(arena, True)

    return arena
