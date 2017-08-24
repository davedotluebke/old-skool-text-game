import thing

def clone():
    branch = thing.Thing('branch', __file__)
    branch.set_description('sturdy oak branch', 'This is a sturdy oak branch. It seems like it could burn for quite a while.')
    branch.add_adjectives('sturdy', 'oak')
    return branch