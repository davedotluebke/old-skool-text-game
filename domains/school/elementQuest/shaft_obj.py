import container

def clone():
    s = container.Container('shaft', __file__)
    s.set_description('shaft of sunlight', 'This is a shaft of warm sunlight coming into the room.', unlisted=True)
    s.add_adjectives('sunlight', 'warm')
    s.add_names('sunlight')
    s.see_inside = True
    s.fix_in_place('You can\'t take sunlight!')
    return s
