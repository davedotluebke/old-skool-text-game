import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    great_hall = room.Room('great hall', safe=True, indoor=True, pref_id=roomPath)
    great_hall.set_description('Great Hall', 'You stand in the biggest room in the entire school, '
        'and it is _enormous_. It is made of ancient stones. A giant banquet table fills the room. '
        'To the north there stands a huge fireplace, the logs in it burning slowly. '
        'To the east a grand staircase rises to an elevated landing.')
    great_hall.add_names('hall', 'chamber')
    great_hall.add_adjectives('grand', 'enormous')
    great_hall.add_exit('west', 'domains.school.school.grand_entry')
    great_hall.add_exit('east', 'domains.school.school.landing')
    
    fireplace = gametools.clone('domains.school.school.fireplace')
    great_hall.insert(fireplace)

    table = gametools.clone('domains.school.school.banquet_table')
    great_hall.insert(table)
    return great_hall
