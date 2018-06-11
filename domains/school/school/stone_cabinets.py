import container
import gametools

def clone():
    cabinets = container.Container('cabinets', __file__)
    cabinets.set_description('bunch of cabinets', 'These cabinets are made of stone, and set into the wall.', unlisted=True)
    cabinets.fix_in_place("How do you think you can take cabinets! You can\'t.")
    cabinets.add_names('cabinet')
    cabinets.add_adjectives('stone', 'inset','strong')
    cabinets.set_max_volume_carried(5000)
    cabinets.set_max_weight_carried(100000)
    cabinets.plural = True
    cabinets.closable = True
    cabinets.close()

    cup = gametools.clone('domains.school.school.cup')
    cabinets.insert(cup, True)      

    return cabinets
