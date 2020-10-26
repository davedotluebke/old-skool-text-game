import creature
import gametools
import thing

def clone():
    orc = creature.NPC('orc', __file__, aggressive=2)
    orc.set_description('orc chieftan', 'This huge powerful orc towers over you.  He is well '
                        'armed and armored, with a high crested helmet that makes him seem even taller.')
    orc.add_adjectives('orc', 'huge', 'powerful', 'tall')
    orc.add_names('chief', 'chieftan')
    orc.set_combat_vars(40, 70, 70, 45)
    orc.act_frequency = 2
    orc.set_max_weight_carried(50000)
    orc.set_max_volume_carried(100)
   
    sword = gametools.clone("domains.centrata.orc_quest.orc_scimitar")
    sword.move_to(orc)

    plate = gametools.clone("domains.centrata.orc_quest.orc_plate")
    plate.move_to(orc)

    helmet = gametools.clone("domains.centrata.orc_quest.orc_helmet")
    helmet.move_to(orc)

    return orc