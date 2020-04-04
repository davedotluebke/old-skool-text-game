import gametools
import room
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    lookout = room.Room('lookout', safe=True, pref_id=roomPath)
    lookout.indoor = True
    lookout.set_description('circular lookout', 'This lookout oversees the entire school and surrounding area. With 360 degree views, you see:'+  \
'\n'+'a thick forest \n'+'a little house \n'+'a garden \n'+'a distant mountain range \n'+'more thick forest and some school grounds \n'+'and even more forest that stretches on for hundreds of [IMP]miles[/IMP][SI]kilometres[/SI]')
    lookout.add_adjectives('circular')
    lookout.add_exit('down', 'domains.school.school.towerstairs')

    thick_forest = scenery.Scenery('forest', 'thick forest',
        'This is some thick forest surrounding the school grounds. '
        'You think you might see something suspended in the trees, but you can\'t be sure.', unlisted=True)
    thick_forest.add_adjectives('thick')
    thick_forest.move_to(lookout, True)

    garden = scenery.Scenery('garden', 'school garden',
        'This school garden appears to have a large variety of plants growing in it. '
        'You can make out some truly large sunflowers.', unlisted=True)
    garden.add_adjectives('school')
    garden.move_to(lookout, True)

    mountain_range = scenery.Scenery('range', 'mountain range',
        'This distant mountain range is very tall. You can make out large snow-covered areas.', unlisted=True)
    mountain_range.add_adjectives('distant', 'mountain', 'snow-covered')
    mountain_range.add_names('mountains')
    mountain_range.move_to(lookout, True)

    return lookout
