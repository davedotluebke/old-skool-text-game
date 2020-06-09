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
    r.set_description('circular carpeted room', 'You find yourself in a tidy circular room that is carpeted with a cozy red carpet. A beautiful gold statue of a bird atop a dark marble stand in the center of the room catches your eye. On the edge of the room, against the wall some wooden stairs lead up to the next level')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.portait_gallery')
    r.add_exit('down', 'domains.school.elementQuest.windy_hall')
    r.add_exit('west', 'domains.school.elementQuest.china_closet')
    r.add_exit('east', 'domains.school.elementQuest.wardrobe_room')

    stand = scenery.Scenery ('stand', 'dark marble stand', 'This is a tall stand made of dark marble, atop it is a beautiful gold statue of a bird. On the side of the stand there is a plaque.', unlisted=True)
    stand.add_names('stand')
    stand.add_adjectives('dark', 'marble', 'tall')
    r.insert(stand)

    statue = scenery.Scenery ('statue', 'golden statue of a bird', 'This is a intricate statue of a swallow atop a marble stand. It looks like it was carved by hand out of pure gold.', unlisted=True)
    statue.add_names('statue')
    statue.add_adjectives('intricate', 'gold', 'hand-carved', 'sollow')
    r.insert(statue)

    plaque = scenery.Scenery ('plaque', 'wooden plaque about statue', 'This is a spruce plaque about the statue. It looks like it was hand-carved and the letters are lined with pure gold.', unlisted=True)
    plaque.add_names('plaque')
    plaque.add_adjectives('spruce', 'wood', 'wooden')
    plaque.add_response(['read'], 'The plaque reads: \n Swallows fly hi and low \n Searching for food in the snow \n Some wounder where they go \n But only they know')
    r.insert(plaque)
    
    return r
