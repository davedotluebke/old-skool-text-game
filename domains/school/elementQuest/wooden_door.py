import thing
import player
import action

class Door(thing.Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self):
        super().__init__('door', __file__)
        self.set_description('wooden door', 'This thick wooden door is made of strong wood. There is no handle.')
        self.add_adjectives('wooden', 'thick')

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def burn(self, obj):
        if obj.names[0] == 'torch':
            if obj.lit:
                self.emit('The wooden door burns in a flickering of flames.')
                if isinstance(obj.location, player.Player):
                    obj.location.cons.write("You can't hold onto the torch anymore, it's burning everywhere.")
                obj.move_to(thing.Thing.ID_dict['nulspace'])
                self.emit('You can now go through the doorway to the west.')
                self.location.add_exit('west', 'domains.school.elementQuest.portal_room')
                self.location.extract(self)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    def open(self, p, cons, oDO, oIDO):
        if oDO == self:
            cons.write('You try to open the door, but it is locked from the other side.')
            return True
        return "Did you mean to open the door?"

    actions = dict(Thing.actions)  # make a copy
    actions['open'] = Action(open, True, False)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def clone():
    return Door()