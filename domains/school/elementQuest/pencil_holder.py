import container
import gametools

def clone():
    pencil_holder = container.Container('holder', __file__)
    pencil_holder.set_description('wooden pencil holder', 'This is a plain wooden pencil holder.')
    pencil_holder.add_adjectives('wooden', 'plain', 'pencil')
    pencil_holder.set_flammable(2)
    pencil_holder.burn_time = 25
    pencil_holder.set_max_volume_carried(0.125)
    pencil_holder.set_max_weight_carried(100)

    pencil = gametools.clone('domains.school.elementQuest.pencil')
    pencil.plurality = 9
    pencil_holder.insert(pencil)
    
    return pencil_holder
