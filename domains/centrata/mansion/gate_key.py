import thing

def clone():
    key = thing.Thing('key', __file__)
    key.set_description('heavy iron key', 'This is a heavy key made of iron.')
    key.add_adjectives('heavy', 'iron')
    return key
