import thing

def clone():
    cave_moss = thing.Thing('cave moss', __file__)
    cave_moss.set_description('cave moss', 'This is some strange moss growing in the cave.')
    cave_moss.add_adjectives('cave')
    cave_moss.add_names('moss')
    return cave_moss
