import container
import gametools

def clone():
    cabinets = container.Container('cabinet', __file__)
    cabinets.set_description('lightly stained wood cabinet', 'This lightly stained wooden cabinet is slightly dusty.')
    cabinets.fix_in_place("You cannot take cabinets.")
    cabinets.add_adjectives('wood', 'lightly stained','stained','old','1960s',"1960's",'60s',"60's")
    cabinets.set_max_volume_carried(5000)
    cabinets.set_max_weight_carried(100000)
    cabinets.plurality = 3
    cabinets.closable = True
    cabinets.close()

    flask = gametools.clone('domains.school.forest.flask')
    cabinets.insert(flask)

    return cabinets