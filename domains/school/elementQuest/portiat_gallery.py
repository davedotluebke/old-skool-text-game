import room
import gametools
import thing
import scenery


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('hall', roomPath)
    r.indoor = True
    r.set_description('airy portriat gallery', 'You find yourself in a airy circler room. The walls are lined with many differnt portriats of birds. There is a plaque on the north wall. On the edge of the room, against the wall some wooden stairs lead up to the next level. The floor is made of smooth stone and well polished.')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.armor_museum')
    r.add_exit('down', 'domains.school.elementQuest.statue_room')
    r.add_exit('east', 'domains.school.elementQuest.sauna_room')
''


    
    dark_portriat = scenery.Scenery ('dark portriat', 'dark portriat', 'This portriat depicts a great horned out on a hunt in the dark of night. It is painted in oil paint.')
    dark_portriat.add_names('portriat', 'painting')
    dark_portriat.add_adjectives('dark', 'owl', 'night', 'oil')
    r.insert(dark_portriat)

    watercolor_portriat = scenery.Scenery ('watercolor portriat', 'watercolor portriat', 'This is a watercolor portriat. It depicts a eastern bluebird feeding its young on its nest in the branches of a beach tree. It makes you feel happy and hopefull.')
    watercolor_portriat.add_names('portriat', 'painting')
    watercolor_portriat.add_adjectives('light', 'bluebird', 'birdhouse', 'watercolor', 'water color')
    r.insert(watercolor_portriat)

    patel_portriat = scenery.Scenery ('pastel portriat', 'pastel portriat', 'This is a vivid portriat that depicts a a flock of parrots on a branch in the jungle. Its colors impress you.')
    patel_portriat.add_names('portriat', 'painting')
    patel_portriat.add_adjectives('bright', 'parrot', 'jungle', 'pastel')
    r.insert(patel_portriat)

    plaque = scenery.Scenery ('plaque', 'metal plaque on wall', 'This is a normal metal plaque', unlisted=False)
    plaque.add_names('plaque')
    plaque.add_adjectives('metal', 'normal')
    plaque.add_response(['read'], 'The plaque reads: Please do not touch any of the paintings. \n No flash photography \n No food or drink in the gallery')
    r.insert(plaque)
    
    return r
