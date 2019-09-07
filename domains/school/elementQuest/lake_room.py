import room
from thing import Thing
from action import Action
import gametools

class LakeRoom_surface(room.Room):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, roomPath, underwater_loc):
        super().__init__(default_name, roomPath)
        self.underwater_loc = underwater_loc

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def dive(self, p, cons, oDO, oIDO):
        cons.user.perceive('You dive under the lake and find yourself in a different environment.')
        cons.user.emit('&nd%s dives underwater and disappears from sight.' % cons.user)
        loc = gametools.load_room(self.underwater_loc)
        cons.user.move_to(loc)
        Thing.game.events.schedule(Thing.game.time+15, loc.force_surface, cons.user)
        return True
    
    actions = dict(room.Room.actions)  # make a copy
    actions['dive'] = Action(dive, False, True)
    actions['swim'] = actions['walk']  # replace walk with swim
    del actions['walk']

class LakeRoom_underwater(room.Room):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, roomPath, surface_loc):
        super().__init__(default_name, roomPath)
        self.surface_loc = surface_loc

    #
    # OTHER EXTERNAL METHODS (callbacks & misc externally visible methods)
    #
    def force_surface(self, user):
        if user not in self.contents:
            if isinstance(user.location, LakeRoom_underwater):
                user.location.force_surface(user)
            return
        if user.wizardry_element == 'water': #if the user is already a water wizard, then they don't have to re-surface
            return
        user.perceive('You find that you are out of air and must resurface.')
        user.emit('&nD%s swims upward and disappears from sight.' % user)
        loc = gametools.load_room(self.surface_loc)
        user.move_to(loc)
        user.emit('&nD%s surfaces.' % user)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def surface(self, p, cons, oDO, oIDO):
        cons.user.perceive('You swim upwards and resurface.')
        cons.user.emit('&nD%s swims upwards and disappears from sight.')
        loc = gametools.load_room(self.surface_loc)
        cons.user.move_to(loc)
        return True
    
    actions = dict(room.Room.actions)  # make a copy
    actions['surface'] = Action(surface, False, True)
    actions['swim'] = actions['walk']  # replace walk with swim
    del actions['walk']