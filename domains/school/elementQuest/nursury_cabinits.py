import container
import gametools

def clone():
    nursury_cabinits = container.Container('cabinits', 'cabinits', 'These are some white painted wood cabinits. One of them has a painting of a mockingbird painted on it.')
    nursury_cabinits.add_names('cooler', 'box')
    nursury_cabinits.add_adjectives('ice', 'cooler', 'cooling', 'cold')
    nursury_cabinits.closable = True

    baby_toy_1 = gametools.clone('domains.school.elementQuest.baby_toy_1')
    baby_toy_2 = gametools.clone('domains.school.elementQuest.baby_toy_2')
    baby_toy_3 = gametools.clone('domains.shcool.elementQuest.baby_toy_3')

    nursury_cabinits.set_max_volume_carried(100)
    nursury_cabinits.set_max_weight_carried(50000)
    nursury_cabinits.fix_in_place('The cabinits are atached to the floor so you can\'t move them.')
    nursury_cabinets.closable = True


    nursury_cabinits.insert(baby_toy_1)
    nursury_cabinits.insert(baby_toy_2)
    nursury_cabinits.insert(baby_toy_3)

    nursury_cabinits.close()

    return nursury_cabinits
