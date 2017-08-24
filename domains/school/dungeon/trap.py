import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    trap = room.Room('gold room', roomPath)
    trap.set_description('room with gold in the center', 'You are in a large room. In the center of the room is a big pile of gold coins.')
    trap.add_exit('east', 'domains.school.dungeon.small_tunnel')
    trap.add_names('room', 'trap')
    trap.add_adjectives('gold')

    gold = gametools.clone('domains.school.dungeon.gold')
    trap.insert(gold)
    return trap
