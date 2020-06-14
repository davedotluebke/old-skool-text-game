import container

def clone():
    cabinets = container.Container('cabinet', __file__)
    cabinets.set_description('titanium cabinet', 'This cabinet is made of solid titanium.')
    cabinets.fix_in_place("The cabinets are fixed to the wall - securely.")
    cabinets.add_adjectives('metal', 'titanium','strong')
    cabinets.set_max_volume_carried(5000)
    cabinets.set_max_weight_carried(100000)
    cabinets.plurality = 3
    cabinets.closable = True
    cabinets.close()

    return cabinets
