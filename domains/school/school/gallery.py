import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    gallery = room.Room('gallery', safe=True, pref_id=roomPath)
    gallery.indoor = True
    gallery.set_description('portrait gallery', "This grandiose portrait gallery overlooks the Great Hall through a pillared colonnade.")
    gallery.add_exit('east', 'domains.school.school.landing')
    gallery.add_exit('north', 'domains.school.school.hmasters_office')
    gallery.add_exit('northeast', 'domains.school.school.hallway')
    return gallery
