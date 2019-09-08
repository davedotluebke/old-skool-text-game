import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    potion_storage = room.Room('potion storage', safe=True, pref_id=roomPath)
    potion_storage.indoor = True
    potion_storage.set_description('potion storage room', 'This is a stone-walled potion storage room that is dimly lit. It has many cauldrons on an open shelf and many burners for heating cauldrons. It has many ingredients on a different open shelf across the room.'
    'You have to step carefully here, as the floor is covered in shards of broken glass.')
    potion_storage.add_names('potion', 'storage')
    potion_storage.add_names('room')
    potion_storage.add_exit('up', 'domains.school.school.library')

    cauldron = gametools.clone('domains.school.school.cauldron')
    potion_storage.insert(cauldron)

    scale = gametools.clone('domains.school.school.dragon_scale')
    potion_storage.insert(scale)
    return potion_storage
