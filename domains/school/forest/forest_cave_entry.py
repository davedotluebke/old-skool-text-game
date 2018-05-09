import gametools
import scenery
import room
import action
import thing

class Vines(scenery.Scenery):
    def __init__(self, default_name, short_desc, long_desc):
        super().__init__(default_name, short_desc, long_desc)
        self.actions.append(action.Action(self.clear, ['clear', 'remove'], True, False))

    def clear(self, p, cons, oDO, oIDO):
        if oDO != self:
            return 'What do you want to clear?'
        cons.user.perceive('You clear the vines away, revealing a cave entrance to the north.')
        self.emit('&nD%s clears the vines away, revealing a cave entrance to the north.',[cons.user])
        self.location.add_exit('north','domains.school.forest.abandoned_fire')
        self.location.set_description('forest cave entry','You find yourself in front of a hill with a cave entrance.')
        self.move_to(thing.Thing.ID_dict['nulspace'])
        return True

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('forest_cave_entry',roomPath)
    r.set_description('forest hill','You find yourself in front of a hill. The hill is covered by a wall of vines.')
    r.add_exit('east', 'domains.school.forest.gloomy_forest')

    vine_obj = Vines('vines','wall of vines','The vines are thick and tangled, but seem to move freely.')
    vine_obj.move_to(r, force_move=True)
    return r
