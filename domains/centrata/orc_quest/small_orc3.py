import gametools
import thing
from domains.centrata.orc_quest.orc import Orc

def clone():
    orc = Orc('orc', __file__, aggressive=2)
    orc.set_orc_range(5)
    orc.set_description('flabby orc', "This flabby, enormously fat orc doesn't look particularly fast, but you "
        "don't want to make it angry. Oops, too late, it's already angry!")
    orc.add_adjectives('flabby', 'fat', 'angry')
    orc.set_combat_vars(30, 40, 55, 30)
    orc.act_frequency = 4

    spike = gametools.clone("domains.centrata.orc_quest.orc_spike")
    spike.move_to(orc)
    return orc