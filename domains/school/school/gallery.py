import gametools
import room
import scenery

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    gallery = room.Room('gallery', safe=True, pref_id=roomPath)
    gallery.indoor = True
    gallery.set_description('portrait gallery', "This grandiose portrait gallery overlooks the Great Hall through a pillared colonnade.")
    gallery.add_exit('east', 'domains.school.school.landing')
    gallery.add_exit('north', 'domains.school.school.hmasters_office')
    gallery.add_exit('northeast', 'domains.school.school.hallway')

    portrait = scenery.Scenery('portrait','fancy portrait', 'This oil on canvas portrait is of a strange figure. He is dressed in dark colors and is against a dark background.')
    portrait.add_response('take', 'You think about taking the portait for a moment, but then realize that it is the school\'s property and should not steal it.')
    gallery.insert(portait, True)

    portrait_two = scenery.Scenery('portrait','light portait', 'This portrait is over a woman in a sky blue dress, with very long hair. She seems to be in front of a large lake, surrounded by a thick forest.')
    portrait_two.add_response('take', 'You think about taking the portait for a moment, but then realize that it is the school\'s property and should not steal it.')
    gallery.insert(portrait_two, True)

    portrait_three = scenery.Scenery('portrait','bright portait', 'This portait is of a woman and a man in a blazing fire. They almost seem to be performing some sort of meditation exersise.')
    portrait_three.add_response('take', 'You think about taking the portait for a moment, but then realize that it is the school\'s property and should not steal it.')
    gallery.insert(portrait_three, True)

    portrait_four = scenery.Scenery('portrait','seethrough portait', 'This portait is very strange. It is made of glass. You can barely make out a figure in the center.')
    portrait_four.add_response('take', 'You think about taking the portait for a moment, but then realize that it is the school\'s property and should not steal it.')
    gallery.insert(portrait_four, True)

    return gallery
