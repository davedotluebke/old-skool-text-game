import container
import gametools

def clone():
    bed = container.Container('bed', __file__)
    bed.set_description('large bed', 'This large bed faces the window. You notice a beside table next to it.', unlisted=True)
    bed.add_adjectives('large')
    bed.set_prepositions('on', 'onto')
    bed.fix_in_place('The bed is too heavy to move.')
    bed.set_max_volume_carried(7000)
    bed.set_max_weight_carried(4e9)

    duvet = gametools.clone('domains.school.elementQuest.bed')
    bed.insert(duvet)
    
    return bed
