import creature
import gametools
import thing

class Orc(creature.NPC):
    def is_forbidden(self, r):
        # Check whether the creature is allowed to enter room `r`.
        # `r` is string containing the path to the room
        # return True if the room is forbidden
        return False


def clone():
    orc = Orc('orc', __file__, aggressive=2)
    orc.set_description('thin orc', "This thin orc is a loathsome creature that would not hesitate to "
        "stab you in the back or slit your throat in the dark.")
    orc.add_adjectives('thin', 'loathsome')
    orc.set_combat_vars(30, 40, 50, 40)
    orc.act_frequency = 2

    club = gametools.clone("domains.centrata.orc_quest.orc_club")
    club.move_to(orc)
    return orc