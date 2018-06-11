import domains.school.elementQuest.lake_room as lake_room
import room
import gametools
import scenery

class Doorway(scenery.Scenery):
    instance = None
    def __init__(self):
        super().__init__('doorway', 'stone doorway', 'This is a stone doorway, leading to the east. A shimmering surface covers the entrance.')
        self.actions.append(scenery.Action(self.enter, ['enter'], True, False))
        self.state = 'closed'
        Doorway.instance = self
    
    def open(self):
        self.long_desc = 'This is a stone doorway, leading to the east.'
        self.state = 'open'

    def enter(self, p, cons, oDO, oIDO):
        if self.state == "closed":
            cons.user.perceive('You try to enter the doorway, but something blocks your path.')
            return True
        cons.user.wizardry_element = 'water'
        cons.user.perceive('As you swim through the doorway, you start to feel a buildup of pressue. '
                           'Somehow, however, it doesn\'t seem unconfortable. Then, all of the sudden, '
                           'you begin to feel as if you have given in to--no, '
                           'ABSORBED the pressure. You suddenly realize you are in a different place...')
        lounge = gametools.load_room('domains.school.school.water_lounge')
        if lounge and cons.user.move_to(lounge):
            self.emit('&nD%s swims through the doorway, and dissapears on the other side.' % cons.user)
        else:
            cons.user.perceive('...and just as quickly, you feel yourself return! But something has changed...')
        return True


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    coral_room = lake_room.LakeRoom_underwater('coral-filled room', roomPath, 'domains.school.elementQuest.lake_e')
    coral_room.set_description('coral-filled room', 'This part of the lake has a small amount of coral growing. To the east you see a stone doorway.')
    coral_room.add_exit('west', 'domains.school.elementQuest.deep_depths')
    coral_room.add_exit('north', 'domains.school.elementQuest.course_sand')
    coral_room.add_exit('south', 'domains.school.elementQuest.inflow')

    coral_room.insert(Doorway(), True)
    
    return coral_room
