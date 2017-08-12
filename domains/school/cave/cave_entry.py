import domains.school.cave as cave_mod
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    cave_entrance = CaveEntry('cave mouth', roomPath)
    cave_entrance.add_aditional_vars('domains.school.forest.forest3', Thing.ID_dict['nulspace'].game)
    cave_entrance.add_exit('east', 'domains.school.forest.forest3')
    cave_entrance.add_exit('in', 'domains.school.cave.cave')
    return cave_entrance
