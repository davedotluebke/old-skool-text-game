import gametools
import room
import scenery

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

    glass = scenery.Scenery('glass', 'broken glass', 'These shards of broken glass cover the floor. Evidently there have been some explosions here in the past.', unlisted=True)
    glass.add_adjectives('broken')
    glass.add_names('shards')
    glass.add_response(['take', 'sweep', 'clean'], 'The glass shards are too small to easy clean off the floor.')
    potion_storage.insert(glass, True)

    return potion_storage
