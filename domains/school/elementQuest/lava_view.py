import room
import gametools
import thing
import scenery

class LavaBridge(scenery.Scenery):
    def __init__(self):
        super().__init__('bridge', 'stone drawbridge', 'This stone drawbridge crosses the lava lake. It is currently open.')
        self.add_names('drawbridge')
        self.add_adjectives('stone', 'open')
    
    def lower_drawbridge(self):
        self.remove_adjectives('open')
        self._long_desc = 'This stone drawbridge crosses the lava lake. It is currently lowered, enabling people to cross.'
        self.location._long_desc = self.location._long_desc.replace('It is currently open.', 'It is currently closed.')
        self.location.add_exit('northeast', 'domains.school.elementQuest.portal_room')
        self.emit('The drawbridge lowers into place, now spanning the lava lake.')

    def raise_drawbridge(self):
        # XXX this is never called
        self.add_adjectives('open')
        self._long_desc = 'This stone drawbridge crosses the lava lake. It is currently open.'
        self.location._long_desc = self.location._long_desc.replace('It is currently closed.', 'It is currently open.')
        del self.location.exits['northeast']

class Rope(scenery.Scenery):
    def __init__(self, bridge_obj):
        super().__init__('rope', 'thick rope', 'This thick rope extends down from an unknown point above you to the end of the raised drawbridge. It is clearly holding the drawbridge up.')
        self.add_adjectives('strong', 'thick')
        self.add_response(['take', 'get'], 'The rope is tied firmly and cannot be moved.')
        self.add_response(['tie'], 'The rope is already tied!')
        self.add_response(['untie'], 'You try to untie the rope from the end of the drawbridge, but the knot is too well made.')
        self.add_response(['cut', 'slice', 'attack'], 'Despite your best attempts, the rope strangely cannot be cut.')
        self.bridge_obj = bridge_obj
        self.flammable = 8
    
    def when_lit(self, p, cons, oDO, oIDO):
        cons.user.perceive('You light the rope on fire.')
        self.emit('&nD%s lights the rope on fire.' % cons.user)
        self.emit('The drawbridge begins to lower itself down.')
        cons.game.schedule_event(3, self.bridge_obj.lower_drawbridge)
        self.destroy()
        return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('overlook', roomPath)
    r.indoor = True
    r.set_description('high overlook', 'You discover yourself on a high platform overlooking a large lake of lava. A stone drawbridge spans the pool. It is currently open.')
    r.add_adjectives('high')
    r.add_exit('southeast', 'domains.school.elementQuest.staircase')

    bridge = LavaBridge()
    bridge.move_to(r, True)

    rope = Rope(bridge)
    rope.move_to(r, True)
    return r
