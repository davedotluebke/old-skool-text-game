import thing

def clone():
    log = thing.Thing('log', __file__)
    log.set_description('sturdy log','This log is about [IMP]two feet[/IMP][SI]60 centimetres[/SI] long, and looks far more stable than the rest.')
    log.flammable = 10
    log.add_adjectives('sturdy')
    return log