import gametools
import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    lookout = room.Room('lookout', safe=True, pref_id=roomPath)
    lookout.set_description('circular lookout', 'This lookout looks over the entire school and surrounding area. With 360 degree views, you see:'+  \
'\n'+'a thick forest \n'+'a little house \n'+'a garden \n'+'a distant mountain range \n'+'more thick forest, and some school grounds \n'+'even more forest that streaches on for hundreds of miles')
    lookout.add_adjectives('circular')
    lookout.add_exit('down', 'domains.school.school.towerstairs')
    return lookout
