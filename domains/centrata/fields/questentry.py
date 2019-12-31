import gametools
import scenery
import room
import action

class sinkholeLake(scenery.Scenery):
    def __init__(self):
        super().__init__('lake', 'beautiful lake', 'This beautiful lake looks quite cool compared to the hot sun you are feeling now.')
        self.actions['enter'] = action.Action(sinkholeLake.enter, True, False)
        self.actions['dive'] = action.Action(sinkholeLake.enter, True, True)
    
    def enter(self, p, cons, oDO, oIDO):
        cons.write('''You enter the lake, feeling much cooler than you were before.
                    All of the sudden you feel yourself getting pulled into
                    the centre of the lake and into a sinkhole! Somehow, however, you 
                    seem to find yourself in a new place...''')
        cons.user.move_to(gametools.load_room('domains.centrata.key_quest.bat_fight'))
        return True
        

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    lakeside = room.Room('lakeside', roomPath)
    lakeside.set_description('shore of a lake', 'You find yourself beside a large lake with a shallow shoreline. The sun shines brightly here. The lakewaters seem as if they might be cooler.')
    lakeside.add_adjectives('hot')
    lakeside.add_exit('west', 'domains.centrata.fields.road_six')

    lake = sinkholeLake()
    lakeside.insert(lake, True)

    return lakeside
