import container
import gametools

def clone():
    nursury_cabinets = container.Container('cabinets', __file__)
    nursury_cabinets.set_description('cabinets', 'These are some white painted wood cabinets. One of them has a painting of a mockingbird painted on it.')
    nursury_cabinets.add_names('cooler', 'box')
    nursury_cabinets.add_adjectives('ice', 'cooler', 'cooling', 'cold')
    nursury_cabinets.closable = True

    baby_toy_1 = gametools.clone('domains.school.elementQuest.baby_toy_1')
    baby_toy_2 = gametools.clone('domains.school.elementQuest.baby_toy_2')
    baby_toy_3 = gametools.clone('domains.shcool.elementQuest.baby_toy_3')

    nursury_cabinets.set_max_volume_carried(100)
    nursury_cabinets.set_max_weight_carried(50000)
    nursury_cabinets.fix_in_place('The cabinets are atached to the floor so you can\'t move them.')
    nursury_cabinets.closable = True


    nursury_cabinets.insert(baby_toy_1)
    nursury_cabinets.insert(baby_toy_2)
    nursury_cabinets.insert(baby_toy_3)

    nursury_cabinets.close()

    return nursury_cabinets
