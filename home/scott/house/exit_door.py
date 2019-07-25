import scenery
import gametools
import creature
import action

class Door(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc, dest, direction, allowed_players=None):
        super().__init__(default_name, short_desc, long_desc)
        self.dest = dest
        self.direction = direction
        self.add_adjectives(direction)
        self.actions['open'] = action.Action(Door.enter_door, True, False)
        self.actions['enter'] = action.Action(Door.enter_door, True, False)
        self.unlisted = True
    
    def enter_door(self, p, cons, oDO, oIDO):
        if self != oDO:
            return "Did you mean to open and go through the door?"
        dest_room = gametools.load_room(self.dest)
        if not dest_room:
            return "For some reason you are unable to go through the door."
        cons.user.move_to(dest_room)
        cons.user.emit('&nD%s opens the door and passes through it.' % cons.user)
        cons.user.perceive('You pass through the door and find yourself in a new location.')
        cons.user.location.report_arrival(cons.user)
        return True

class Window(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc, view_of):
        super().__init__(default_name, short_desc, long_desc)
        self.unlisted = True
        self.view_of = gametools.load_room(view_of)
        self.windowWatcher = gametools.clone('home.scott.house.windowWatcher') #XXX this should be dynamic with any file placement
        self.windowWatcher.move_to(self.view_of)
        self.windowWatcher.window_obj = self
        del self.actions['look']
        self.actions['look'] = action.Action(Window.look_at, True, False)
    
    def look_at(self, p, cons, oDO, oIDO):
        if self == oDO or self == oIDO:
            cons.user.perceive(self.long_desc)
            cons.user.perceive('Through the window you see:')
            try:
                self.view_of.look_at(p, cons, oDO, oIDO)
                return True
            except AttributeError:
                cons.user.perceive('an AttributeError')
                return True
        else:
            return "Not sure what you're trying to look at!"
    
    def change_view(self, new_view_of):
        self.view_of = gametools.load_room(new_view_of)
        self.windowWatcher.move_to(self.view_of)

    def get_window_message(self, message):
        self.emit('Through the window you notice: '+str(message))
