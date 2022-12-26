import room
import gametools

class AirBridgeRoom(room.Room):
    def go_to(self, p, cons, oDO, oIDO):
        if p.words[1] == 'north' and cons.user.wizardry_element != 'air':
            cons.user.perceive('The stone bridge to the north appears to be too broken to cross.')
            return True
        return super().go_to(p, cons, oDO, oIDO)
    
    def look_at(self, p, cons, oDO, oIDO):
        return_value = super().look_at(p, cons, oDO, oIDO)
        if return_value == True and cons.user.wizardry_element == 'air':
            cons.user.perceive('A rainbow shines down on the stone bridge to the north, making it look like a pathway.')
        return return_value

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    air_bridge = AirBridgeRoom('rooftop', roomPath, safe=True)
    air_bridge.set_description('tall tower', 'You find yourself on the open top of a tower overlooking the school building. A taller tower rises above you to the west. To the north a crumbling stone archway bridge leads to the top of another tower.')
    air_bridge.add_exit('down', 'domains.school.school.tower2')
    air_bridge.add_exit('north', 'domains.school.school.air_lounge')
    return air_bridge
