import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    hmasters_office = room.Room('office', safe=True, pref_id=roomPath)
    hmasters_office.indoor = True
    hmasters_office.set_description('grandiose headmasters office', 'You look at a giant room with a large bay window in the back. There is a giant carved oak desk in the middle of the room. There are many bookcases lining the walls, and stacks of papers on the desk.')
    hmasters_office.add_adjectives("grandiose", 'headmaster\'s')
    hmasters_office.add_exit('south', 'domains.school.school.gallery')

    desk = gametools.clone('domains.school.school.desk')
    hmasters_office.insert(desk, True)
    return hmasters_office
