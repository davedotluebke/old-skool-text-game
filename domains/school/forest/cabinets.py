import container
import gametools

def clone():
    cabinets = container.Container('cabinets', __file__)
    cabinets.set_description('bunch of cabinets', 'The lightly stained wooden cabinets in this kitchen are slightly dusty.')
    cabinets.fix_in_place("How do you think you can take cabinets!? You can\'t.")
    cabinets.add_names('cabinet')
    cabinets.add_adjectives('wood', 'lightly stained','stained','old','1960s',"60's")
    cabinets.set_max_volume_carried(5000)
    cabinets.set_max_weight_carried(100000)
    cabinets.plural = True
    cabinets.closable = True
    cabinets.close()

    flask = gametools.clone('domains.school.forest.flask')
    cabinets.insert(flask)

    return cabinets