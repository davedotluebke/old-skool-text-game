import scenery
import gametools
import creature
import action

class Door(scenery.Scenery):
    opposite_directions = {
        'north':     'south',
        'south':     'north',
        'east':      'west',
        'west':      'east',
        'down':      'up',
        'up':        'down',
        'northwest': 'southeast',
        'northeast': 'southwest',
        'southeast': 'northwest',
        'southwest': 'northeast'
    }
    def __init__(self, default_name, short_desc, long_desc, dest, direction, allowed_to_lock=['scott', 'isla']):
        super().__init__(default_name, short_desc, long_desc)
        self.dest = dest
        self.direction = direction
        self.add_adjectives(direction)
        self.actions['open'] = action.Action(Door.enter_door, True, False)
        self.actions['enter'] = action.Action(Door.enter_door, True, False)
        self.actions['lock'] = action.Action(Door.lock_door, True, False)
        self.actions['unlock'] = action.Action(Door.unlock_door, True, False)
        self.unlisted = True
        self.locked = False
        self.allowed_to_lock = allowed_to_lock
    
    def toggle_matching(self, lock_setting):
        try:
            r = gametools.load_room(self.dest)
            for i in r.contents:
                if isinstance(i, Door) and i.direction == Door.opposite_directions[self.direction]:
                    i.locked = lock_setting
        except:
            return

    def enter_door(self, p, cons, oDO, oIDO):
        if self != oDO:
            return "Did you mean to open and go through the door?"
        if self.locked:
            cons.user.perceive("The door is locked.")
            return True
        dest_room = gametools.load_room(self.dest)
        if not dest_room:
            return "For some reason you are unable to go through the door."
        cons.user.move_to(dest_room)
        cons.user.emit('&nD%s opens the door and passes through it.' % cons.user)
        cons.user.perceive('You pass through the door and find yourself in a new location.')
        cons.user.location.report_arrival(cons.user)
        return True
    
    
    def lock_door(self, p, cons, oDO, oIDO):
        if self.locked:
            return "The door is already locked!"
        if self.allowed_to_lock != 'everyone' and cons.user.names[0] not in self.allowed_to_lock:
            cons.user.perceive('You don\'t have the key.')
        self.locked = True
        self.toggle_matching(True)
        cons.user.perceive('You lock the door.')
        cons.user.emit('&nD%s locks the door.')
        return True

    def unlock_door(self, p, cons, oDO, oIDO):
        if not self.locked:
            return "The door is already unlocked!"
        if self.allowed_to_lock != 'everyone' and cons.user.names[0] not in self.allowed_to_lock:
            cons.user.perceive('You don\'t have the key.')
        self.locked = False
        self.toggle_matching(False)
        cons.user.perceive('You unlock the door.')
        cons.user.emit('&nD%s unlocks the door.')
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
            cons.user.perceive(self._long_desc)
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
