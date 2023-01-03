import thing

def clone():
    rope = thing.Thing('rope', __file__)
    rope.set_description('strong rope', 'This strong rope looks in good condition.')
    rope.add_adjectives('strong')

    rope.set_weight(1000)
    rope.set_volume(1)
    
    return rope
