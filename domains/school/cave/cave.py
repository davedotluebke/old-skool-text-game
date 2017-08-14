import domains.school.caveComplex as cave_mod
import room
import gametools
import thing

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    lair = gametools.load_room('domains.school.cave.lair')
    cave = cave_mod.CaveRoom('cave', roomPath, lair)
    cave.set_description('terrifying dark cave', 'This is one of the most scary caves you have ever been in. You are anxiousley looking around to see if there are any monsters.')
    cave.add_adjectives('scary', 'dark', 'terrifying')
    cave.add_exit('west', 'domains.school.cave.lair')
    cave.add_exit('east', 'domains.school.forest.forest3')
    thing.Thing.ID_dict['nulspace'].game.register_heartbeat(cave)
    cave.attach_monster(lair.monster)
    return cave
