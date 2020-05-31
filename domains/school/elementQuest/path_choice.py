import gametools
import room
import thing
import action

class QuestDoor(thing.Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path):
        super().__init__(default_name, path)
        self.fix_in_place('The door is strongly secured in place. You can\'t take it.')
        self.opened = False
        self.view_through_door = None
        self.destination = None
        self.add_adjectives(default_name)
        self.add_names('door', 'quest')
    
    #
    # SET/GET METHODS (methods to set or query attributes)
    #    
    def set_view(self, view_through_door):
        self.view_through_door = view_through_door
    
    def set_dest(self, dest):
        self.destination = dest

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def open(self, p, cons, oDO, oIDO):
        # This door won't open for one who has already walked a different path (completed another door quest)
        if self.opened:
            cons.write('The door is already open!')
            return True
        if cons.user.wizardry_element not in [None, self.names[0]]:
            cons.write('Try as you might, you cannot open the door to the path of %s.' % self.names[0])
            return True
        self.opened = True
        cons.write('You open the door, and see %s.' % self.view_through_door)
        self.emit("&nD%s opens the door to the path of %s." % (cons.user.id, self.names[0]))
        self._long_desc += self.view_through_door
        for i in self.location.contents:
            if isinstance(i, QuestDoor) and i.opened and i != self:
                i.opened = False
                self.emit('The doorway to the path of %s slams closed!' % i.names[0])
        return True
    
    def close(self, p, cons, oDO, oIDO):
        if not self.opened:
            cons.write('The door is already closed!')
            return True
        self.opened = False
        cons.write('You close the door.')
        self.emit("&nD%s closes the door to the path of %s." % (cons.user.id, self.names[0]))
        (head, sep, tail) = self._long_desc.partition(self.view_through_door)
        self._long_desc = head
        return True

    def enter(self, p, cons, oDO, oIDO):
        if not self.opened:
            return "You must open the door before you can pass through it."
        dest = gametools.load_room(self.destination)
        if cons.user.move_to(dest):
            cons.write('With a sense of making a momentous decision, you step through the doorway.')
            dest.report_arrival(cons.user)
            self.emit('&nD%s walks through the doorway to the path of %s.' % (cons.user.id, self.names[0]))
        return True

    actions = dict(thing.Thing.actions)  # make a copy
    actions['open'] =   action.Action(open, True, False)
    actions['close'] =  action.Action(close, True, False)
    actions['shut'] =   action.Action(close, True, False)
    actions['slam'] =   action.Action(close, True, False)
    actions['enter'] =  action.Action(enter, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    path_choice = room.Room('circular room', roomPath)
    path_choice.indoor = True
    path_choice.set_description('circular room with four doors', 'You are in a circular room with four doors and a ladder down. Each of the doors has a sign above it. ' \
    'The one farthest left says "Path of Fire", the one to the right of that says "Path of Water", the second farthest right says "Path of Earth", and the one to the right of that says "Path of Air". ' \
    'There is a ladder in the centre of the room leading down.')
    path_choice.add_exit('down', 'domains.school.school.gallary_east')

    fire = QuestDoor('fire', None)
    fire.set_description('door of fire', 'This door is warm and has a large label above it reading "Fire". ')
    fire.set_view('a circular room with a firepit in the middle')
    fire.set_dest('domains.school.elementQuest.firepit')
    path_choice.insert(fire)

    water = QuestDoor('water', None)
    water.set_description('door of water', 'This door is cool and has a large label above it reading "Water". ')
    water.set_view('a peninsula sticking out into a lake')
    water.set_dest('domains.school.elementQuest.peninsula')
    path_choice.insert(water)

    earth = QuestDoor('earth', None)
    earth.set_description('door of earth', 'This door is made of rock and is very hard. It has a large label above it reading "Earth". ')
    earth.set_view('a steep staircase leading underground')
    earth.set_dest('domains.school.elementQuest.staircase')
    path_choice.insert(earth)

    air = QuestDoor('air', None)
    air.set_description('door of air', 'This door is as light as a feather. It has a large label over it reading "Air". ')
    air.set_view('a blustery autumn day in some woods')
    air.set_dest('domains.school.elementQuest.autumn_forest')
    path_choice.insert(air)
    return path_choice
