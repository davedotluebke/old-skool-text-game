import container
import gametools

def clone():
    cabinets = container.Container('cabinet', __file__)
    cabinets.set_description('stone cabinet', 'This cabinet is made of stone, and set into the wall.', unlisted=True)
    cabinets.fix_in_place("You find yourself unable to tear out a wall to take theese cabinets.")
    cabinets.add_adjectives('stone', 'inset','strong')
    cabinets.set_max_volume_carried(5000)
    cabinets.set_max_weight_carried(100000)
    cabinets.plurality = 3
    cabinets.closable = True
    cabinets.close()

    cup = gametools.clone('domains.school.school.cup')
    cabinets.insert(cup, True)      

    return cabinets
