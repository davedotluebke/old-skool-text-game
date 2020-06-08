import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    gallery_east = room.Room('landing', safe=True, pref_id=roomPath)
    gallery_east.indoor = True
    gallery_east.set_description('landing between staircases', 'This is a '
    'landing between staircases. To the southwest a staircase leads down towards'
    ' the great hall. To the west the landing continues into a portrait gallery.'
    'A spiral staircase also begins here, leading up.')
    gallery_east.add_exit('up', 'domains.school.elementQuest.path_choice')
    gallery_east.add_exit('southwest', 'domains.school.school.landing')
    gallery_east.add_exit('west', 'domains.school.school.gallery')
    return gallery_east
