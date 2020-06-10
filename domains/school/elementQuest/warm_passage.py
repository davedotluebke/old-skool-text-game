import room
import gametools
import thing
import scenery
import container

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('passage', roomPath)
    r.indoor = True
    r.set_description('warm passage', 'You find yourself in a small stone-walled passage. The stones are warm, and radiate heat into the room.')
    r.add_names('room')
    r.add_adjectives('stone', 'walled', 'stone-walled', 'warm')
    r.add_exit('northeast', 'domains.school.elementQuest.shaft_of_sunlight')
    r.add_exit('west', 'domains.school.elementQuest.staircase')

    stones = scenery.Scenery('stone', 'warm stone', 'This stone makes up the walls of the room. It seems to radiate heat, especially on the north side.', unlisted=True)
    stones.add_names('stones')
    stones.add_response(['feel'], 'The stones give off a pleasent warm heat.')
    r.insert(stones)
    return r
