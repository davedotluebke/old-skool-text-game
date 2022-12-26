import thing

def clone():
    ring = thing.Thing('ring', __file__)
    ring.set_description('brass ring', "A small brass ring, masterfully engraved with celtic knots. The knots wrap around a unicorn's head at the front.")
    ring.add_adjectives('brass','unicorn','celtic','metal','small')
    return ring