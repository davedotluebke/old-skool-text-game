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
   
    sword = gametools.clone("domains.centrata.orc_quest.orc_scimitar")
    sword.move_to(orc)

    hide = gametools.clone("domains.centrata.orc_quest.orc_plate")
    hide.move_to(orc)

    return orc