import gametools
import scenery
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    four_worlds_room = room.Room('four_worlds_room', roomPath, safe=True, indoor=True)
    four_worlds_room.set_description('tall circular room', 'You enter a tall room with a circular shape. '
    'The ceiling forms itself into a turret, with no more floors above this one. In the centre of the room '
    'you see a large table with four spaces in it.')
    four_worlds_room.add_adjectives('tall', 'circular')
    four_worlds_room.add_exit('southeast', 'domains.school.school.arena')
    four_worlds_room.add_exit('west', 'domains.school.school.water_kitchen', caution_tape_msg="This door is locked.")
    
    table = scenery.Scenery('table', 'large table', 'This large table stands in the centre of the room. '
    'It seems to be have four different sections - one of red velvet, another of smooth granite, '
    'the third of wood, and the fourth of glass. These sections are all supported by a heavy stone base. '
    'Attached to each of the sections, near the centre of the table, is a stone block with a few heavy bolts '
    'coming out of it. It seems that something used to be displayed here.', unlisted=True)
    table.add_response(['put', 'place', 'set'], 'Something suggests to you that this object does not belong on the table.')
    table.add_adjectives('large', 'velvet', 'granite', 'stone', 'wood', 'glass')
    four_worlds_room.insert(table, True)
    
    # TODO: Allow players win the game by placing the four items on the table
    
    return four_worlds_room
