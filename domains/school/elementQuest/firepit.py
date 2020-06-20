import room
import scenery
import thing
import gametools

class Firepit(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc, pref_id=None, unlisted=False):
        self.lit = False
        super().__init__(default_name, short_desc, long_desc, pref_id=pref_id, unlisted=unlisted)
    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def go_out(self):
        (head, sep, tail) = self._long_desc.partition('It is lit.')
        self._long_desc = head + 'It is unlit.'
        self.emit('The firepit goes out.')

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def when_lit(self, p, cons, oDO, oIDO):
        cons.user.perceive('You light the firepit, sending it into flames.')
        self.emit('&nD%s lights the firepit, sending it into flames.' % cons.user.id)
        (head, sep, tail) = self._long_desc.partition('It is unlit.')
        self._long_desc = head + 'It is lit.'
        thing.Thing.game.schedule_event(20, self.go_out)
        return True

    def take(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) =  p.diagram_sentence(p.words)
        errmsg =  "Did you mean to take a branch from the firepit?"
        if not sDO in ('branch', 'oak branch'):
            return errmsg
        if sPrep == "from" and oIDO != self:
            return errmsg
        for i in cons.user.contents:
            if i.path == 'domains.school.elementQuest.branch':
                cons.user.perceive('You already have a branch. Perhaps you should leave the rest for others.')
                return True
        branch = gametools.clone('domains.school.elementQuest.branch')
        branch.burning = self.lit
        cons.user.insert(branch)
        cons.user.perceive("You take a sturdy oak branch from the firepit.")
        cons.user.emit("&nD%s takes a sturdy oak branch from the firepit." % cons.user.id, [cons.user])
        return True

    # Scenery makes a per-object actions[] list, so add actions in load()

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    firepit_room = room.Room('fireQuest1', roomPath)
    firepit_room.indoor = True
    firepit_room.set_description('large room with a firepit in the middle', 'This large domed room has paintings '
        'of dancing flames on the walls. It has a firepit in the centre that is filled with sturdy oak '
        'branches. The doorway through which you entered is to the northwest. ')
    firepit_room.add_exit('northwest', 'domains.school.elementQuest.path_choice')
    firepit_room.add_exit('southeast', 'domains.school.elementQuest.tapestries')

    firepit = Firepit('firepit', 'copper firepit', 'This copper firepit is filled with sturdy oak branches. It is unlit.')
    firepit.actions['take'] =   room.Action(Firepit.take, True, False)
    firepit.actions['get'] =    room.Action(Firepit.take, True, False)
    firepit_room.insert(firepit)
    return firepit_room
