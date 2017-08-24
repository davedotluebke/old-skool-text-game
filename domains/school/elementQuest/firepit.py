import room
import scenery
import gametools

def light(p, cons, oDO, oIDO):
    pass

def take(p, cons, oDO, oIDO):
    (sV, sDO, sPrep, sIDO) =  p.diagram_sentence(p.words):
    if not sDO == 'branch' and not sDO == 'oak branch':
        return "Did you mean to take a branch?"
    for i in cons.user.contents:
        if i.path == 'domains.school.elementQuest.branch':
            cons.write('You already have a branch. Perhaps you should leave the rest for others.')
            return True
    branch = gametools.clone('domains.school.elementQuest.branch')
    cons.user.insert(branch)
    return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    firepit_room = room.Room('fireQuest1', roomPath)
    firepit_room.set_description('large room with a firepit in the middle', 'This large domed room has paintings of dancing flames on the walls. It has a firepit in the center, currently unlit and filled with sturdy oak branches.')
    firepit_room.add_exit('northwest', 'domains.school.elementQuest.path_choice')
    firepit_room.add_exit('southeast', 'domains.school.elementQuest.TMP')

    firepit = scenery.Scenery('firepit', 'copper firepit', 'This copper firepit is filled with sturdy oak branches. It is unlit.')
    firepit.actions.append(room.Action(light, ['light', 'hold', 'touch', 'put'], True, False))
    firepit.actions.append(room.Action(take, ['take', 'get'], True, False))
    firepit.lit = False
    firepit_room.insert(firepit)
    return firepit_room
