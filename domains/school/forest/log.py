import thing

def clone():
    log = thing.Thing('log', __file__)
    log.set_description('sturdy log','This log is about two feet long, and looks far more stable than the rest.')
    log.flammable = True
    log.add_adjectives('sturdy')
    return log