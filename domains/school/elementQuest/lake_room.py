import room
import thing
import gametools

class LakeRoom_surface(room.Room):
    def __init__(self, default_name, roomPath, underwater_loc):
        super().__init__(default_name, roomPath)
        self.actions.append(room.Action(self.dive, ['dive'], False, True))
        for i in self.actions:
            if i.verblist == ['go', 'walk']:
                i.verblist == ['go', 'swim']
        self.underwater_loc = underwater_loc

    def dive(self, p, cons, oDO, oIDO):
        cons.user.perceive('You dive under the lake and find yourself in a different environment.')
        cons.user.emit('&nd%s dives underwater and disappears from sight.' % cons.user)
        loc = gametools.load_room(self.underwater_loc)
        cons.user.move_to(loc)
        thing.Thing.game.events.schedule(thing.Thing.game.time+15, loc.force_surface, cons.user)
        return True

class LakeRoom_underwater(room.Room):
    def __init__(self, default_name, roomPath, surface_loc):
        super().__init__(default_name, roomPath)
        self.actions.append(room.Action(self.surface, ['surface'], False, True))
        for i in self.actions:
            if i.verblist == ['go', 'walk']:
                i.verblist == ['go', 'swim']
        self.surface_loc = surface_loc

    def force_surface(self, user):
        if user not in self.contents:
            return
        if user.wizardry_element = 'water': #if the user is already a water wizard, then they don't have to re-surface
            return
        user.perceive('You find that you are out of air and must resurface.')
        user.emit('&nD%s swims upward and disappears from sight.' % user)
        loc = gametools.load_room(self.surface_loc)
        user.move_to(loc)
        user.emit('&nD%s surfaces.' % user)

    def surface(self, p, cons, oDO, oIDO):
        cons.user.perceive('You swim upwards and resurface.')
        cons.user.emit('&nD%s swims upwards and disappears from sight.')
        loc = gametools.load_room(self.surface_loc)
        cons.user.move_to(loc)
        return True
