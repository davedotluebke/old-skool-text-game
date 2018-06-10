import domains.school.elementQuest.lake_room as lake_room
import room
import gametools
import scenery
import action
import domains.wizardry.gems as gems

class Statue(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc):
        super().__init__(default_name, short_desc, long_desc)
        self.actions.append(action.Action(self.put_pearl_in_eye, ['put', 'place'], True, False))
        self.unlisted = True

    def put_pearl_in_eye(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO == 'pearl' and sIDO == 'eye' and isinstance(oDO, gems.Pearl):
            cons.user.emit('&nD%s puts the pearl in the eye of the statue.', ignore=[cons.user])
            cons.user.perceive('You put the pearl in the eye of the statue and see it start to glow.')
            #TODO: Add code for opening trapdoor
            return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = lake_room.LakeRoom_underwater('statueroom',roomPath,'domains.school.elementQuest.lake_w')
    r.set_description('pebble-floored room', 'This pebble-floored room has a large statue in the center of it. ')
    r.add_exit('south', 'domains.school.elementQuest.shallow_shore')
    r.add_exit('north', 'domains.school.elementQuest.seaweed_forest')
    r.add_exit('east', 'domains.school.elementQuest.deep_depths')
    
    obj = Statue('statue', 'statue', 'This giant stone statue solemnly stands in the middle of the room. It is missing a pearl in its left eye. ')
    obj.add_adjectives('giant', 'stone')
    obj.move_to(r)
    
    return r
