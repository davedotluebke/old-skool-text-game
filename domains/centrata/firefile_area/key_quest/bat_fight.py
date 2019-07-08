import gametools
import scenery
import room

class BatFightRoom(room.Room):
    def go_to(self, p, cons, oDO, oIDO):
        if p.words[1] == 'south':
            if cons.user not in self.keyhole.checked_players:
                return "I'm not sure how to go south!"
        super().go_to(p, cons, oDO, oIDO)

class Keyhole(scenery.Scenery):
    def __init__(self):
        super().__init__('keyhole', 'keyhole embeded in the rock face', 'This keyhole is embeded in the rock face. You cannot see any other sign of a door.')
        self.unlisted = True
        self.actions.append(scenery.Action(self.open, ['put', 'insert'], True, False))
        self.checked_players = []
    
    def open(self, p, cons, oDO, oIDO):
        if hasattr(oDO, 'qkey_number') and oDO.qkey_number == 1:
            cons.user.perceive('As soon as you insert the key, the massive rock wall begins to part, revealing a passage to the south.')
            self.location.add_exit('south', 'domains.centrata.firefile_area.key_quest.maze_entrance')
            oDO.move_to(room.Thing.ID_dict['nulspace'])
            return True
        else:
            cons.user.perceive("You try to put the %s in the keyhole, but it doesn't fit." % oDO.default_name)
            return True

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = BatFightRoom('cave', roomPath)
    r.set_description('cave', '''You find yourself in a large cave with a mostly flat floor. 
    Stalagtites cover the ceiling, and many matching stalagmites cover the floor. Strangely,
    there seems to be no water here, except a few drips that fall from the ceiling. The only
    obvious opening is a small gap in the ceiling at the north end of the room. There almost 
    seems to be a keyhole in the south wall, but you can't be sure''')

    stalagtite = scenery.Scenery('stalagtite', 'large stalagtite', 'This is a particularly large stalagtite that hangs off of the ceiling.')
    stalagtite.add_response(['climb'], 'Unfortunately, you can\'t mannage to get a hold of the stalagtite, because it is too high.')
    r.insert(stalagtite, True)

    bat = gametools.clone('domains.centrata.firefile_area.key_quest.bat')
    bat.have_key()
    r.insert(bat, True)

    keyhole = Keyhole()
    r.insert(keyhole, True)
    r.keyhole = keyhole

    return r