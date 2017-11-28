import domains.school.elementQuest.lake_room as lake_room
import room
import gametools
import scenery

class Statue(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc):
        super().__init__(default_name, short_desc, long_desc)
        self.actions.append(Action(self.put_pearl_in_eye, ['put', 'place'], True, False))
        self.unlisted = True

    def put_pearl_in_eye(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO == 'pearl' and sIDO == 'eye':
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
    
    obj = Statue('statue', 'statue', 'This giant stone statue solemnly stands in the middle of the room. It is missing a pearl in its left eye. ')
    obj.add_adjectives('giant', 'stone')
    obj.move_to(r)

    return r
