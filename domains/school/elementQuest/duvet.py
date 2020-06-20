import thing

def clone():
    duvet = thing.Thing('duvet', __file__)
    duvet.set_description('duvet cover', 'This thick duvet cover has images of various birds woven into it.')
    duvet.add_names('cover')
    duvet.add_adjectives('duvet', 'bird')
    duvet.set_weight(7000)
    duvet.set_volume(140)
    duvet.set_flammable(4)
    duvet.burn_time = 10
    return duvet
