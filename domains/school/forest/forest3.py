import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    forest_three = room.Room('forest', roomPath)
    forest_three.set_description('ancient forest', 'This is an ancient forest with towering trees. They must be hundreds of years old at least. The trees seem gloomy here. There is a small dark cave to the west.')
    forest_three.add_adjectives('ancient','towering','gloomy')
    forest_three.add_exit('southeast', 'domains.school.forest.forest1' )
    forest_three.add_exit('west', 'domains.school.cave.cave')
    forest_three.add_exit('north', 'domains.school.forest.dark_forest' )

    oak = scenery.Scenery('oak', 'menacing old oak', 'This is an old oak that is leaning over the trail. It seems to be scowling at you. You see some truffles at the base.')
    oak.add_adjectives('menacing', 'old', 'oak')
    oak.add_names('tree')
    oak.add_response(['climb'], "The towering oak looks climbable, but it is a menacing old tree--the most so you have ever seen. So you decide to look around for another tree instead.", emit_message='%s looks up at the tree.')
    oak.add_response(['grab', 'hold', 'touch', 'hug'], "To touch the scary old tree for no reason seems silly and slightly intimidating, so you decide not to. You think that if you saw a nice tree you would hug it.", emit_message='%s looks at the tree trunk.')
    forest_three.insert(oak)

    willow = scenery.Scenery('willow', 'sad weeping willow', 'This is the most mournful weeping willow you have ever seen. You almost cry from looking at it.')
    willow.add_adjectives('weeping','sad','mournful','willow')
    willow.add_names('tree')
    willow.add_response(['climb'], 'You cannot hold onto the branches, and they are over a small river.', emit_message='%s reaches for the willow.')
    willow.add_response(['cry', 'weep'], 'You cry as you look at the willow, but then you see the menacing old oak tree across the path and eventually stop.', False, True, '%s weeps.')
    willow.add_response(['hug', 'hold'], 'This just isn\'t the right tree to hug.')
    forest_three.insert(willow)

    truffles = gametools.clone('domains.school.forest.truffles')
    forest_three.insert(truffles)

    return forest_three