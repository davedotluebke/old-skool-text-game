import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    four_worlds_room = room.Room('four_worlds_room', roomPath, safe=True, indoor=True)
    four_worlds_room.set_description('tall circular room', 'You enter a tall room with a circular shape. '
    'The ceiling forms itself into a turret, with no more floors above this one. In the centre of the room you see a large table with four spaces in it.')
    four_worlds_room.add_adjectives('tall', 'circular')
    four_worlds_room.add_exit('southeast', 'domains.school.school.arena')
    four_worlds_room.add_exit('west', 'domains.school.school.water_kitchen', caution_tape_msg="This door is locked.")
    
    # TODO: Place object in the room to let players win the game
    
    return four_worlds_room
