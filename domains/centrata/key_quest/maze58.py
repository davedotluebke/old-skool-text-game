import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath, light=0, indoor=True)
    r.set_description('dark passage','This is a dark passage, you notice a bunch of cave popcorn in the centre of the room.')
    r.add_exit('northeast', 'domains.centrata.key_quest.maze47')
    r.add_exit('south', 'domains.centrata.key_quest.maze27')

    cave_popcorn = scenery.Scenery('popcorn', 'bunch of cave popcorn', 'This cave popcorn looks like a perfect snack!')
    cave_popcorn.unlisted = True
    cave_popcorn.add_adjectives('cave', 'fresh')
    cave_popcorn.add_response(['eat', 'snack', 'munch'], 'You try a bite and instantly regret it. It taste like nasty minrals')
    cave_popcorn.move_to(r, True)

    return r
