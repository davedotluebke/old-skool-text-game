import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    great_hall = room.Room('great hall', safe=True, pref_id=roomPath)
    great_hall.indoor = True
    great_hall.set_description('Great Hall', 'This is the biggest room in the entire school, '
        'and it is enormous. It is made of ancient stones. A giant banquet table fills the room. '
        'To the east a grand staircase rises to an elevated landing.')
    great_hall.add_names('hall', 'chamber')
    great_hall.add_adjectives('grand', 'enormous')
    great_hall.add_exit('west', 'domains.school.school.grand_entry')
    great_hall.add_exit('east', 'domains.school.school.landing')

    table = gametools.clone('domains.school.school.banquet_table')
    great_hall.insert(table)
    return great_hall
