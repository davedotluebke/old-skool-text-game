from debug import dbg

import room
import scenery
import thing
import gametools

def light(p, cons, oDO, oIDO):
    if oDO.names[0] != 'firepit':
        return "I'm not quite sure what you are trying to light..."
    cons.write('You light the firepit, sending it into flames.')
    self.emit('%s lights the firepit, sending it into flames.' % cons.user)
    (head, sep, tail) = oDO.long_desc.partition('It is unlit.')
    oDO.long_desc = head + 'It is lit.'
    thing.Thing.ID_dict['nulspace'].game.events.schedule(Thing.ID_dict['nulspace'].game.time+20, go_out, oDO)
    return True

def go_out(firepit):
    (head, sep, tail) = firepit.long_desc.partition('It is lit.')
    firepit.long_desc = head + 'It is unlit.'
    self.emit('The firepit goes out.')

def take(p, cons, oDO, oIDO):
    (sV, sDO, sPrep, sIDO) =  p.diagram_sentence(p.words)
    errmsg =  "Did you mean to take a branch from the firepit?"
    if not sDO in ('branch', 'oak branch'):
        return  errmsg
    if sPrep == "from" and oIDO != firepit:
        return errmsg
    for i in cons.user.contents:
        if i.path == 'domains.school.elementQuest.branch':
            cons.write('You already have a branch. Perhaps you should leave the rest for others.')
            return True
    branch = gametools.clone('domains.school.elementQuest.branch')
    cons.user.insert(branch)
    cons.write("You take a sturdy oak branch from the firepit.")
    cons.user.emit("%s takes a sturdy oak branch from the firepit." % cons.user, [cons.user])
    return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    firepit_room = room.Room('fireQuest1', roomPath)
    firepit_room.set_description('large room with a firepit in the middle', 'This large domed room has paintings '
        'of dancing flames on the walls. It has a firepit in the center, currently unlit and filled with sturdy oak '
        'branches. The doorway through which you entered is to the northwest. ')
    firepit_room.add_exit('northwest', 'domains.school.elementQuest.path_choice')
    firepit_room.add_exit('southeast', 'domains.school.elementQuest.tapestries')

    firepit = scenery.Scenery('firepit', 'copper firepit', 'This copper firepit is filled with sturdy oak branches. It is unlit.')
    firepit.actions.append(room.Action(light, ['light', 'hold', 'touch', 'put'], True, False))
    firepit.actions.append(room.Action(take, ['take', 'get'], True, False))
    firepit.lit = False
    firepit_room.insert(firepit)
    return firepit_room
