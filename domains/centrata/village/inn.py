import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    inn = room.Room('inn', roomPath)
    inn.set_description("inn", 
        "You are in the tavern of the village inn.  A cheery fire crackles in the hearth at one end of "
        "the large room.  Several tables with benches fill the room, and the innkeeper himself stands "
        "behind the bar that runs along the north side of the room."
        "To your south you can exit to the street. ")
    inn.add_exit('west', 'domains.centrata.village.street4')

    tables = scenery.Scenery('table', 'sturdy wooden table', 'Several sturdy wooden tables provide '
        'a place for patrons to eat, drink, and swap tales.', unlisted=True)
    tables.add_names('tables')
    tables.add_response(['take', 'get', 'move', 'push', 'pull'], 'The tables are too heavy to move.')
    tables.move_to(inn, True)

    fire = scenery.Scenery('fire', 'cheery fire', "A large fire crackles cheerfully in the stone "
        "hearth at the end of the room.", unlisted=True)
    fire.add_adjectives('cheery', 'large', 'cheerful', 'crackling')
    fire.add_response(['cook', 'heat', 'bake'], "There's no easy way to use the fire for cooking.")
    fire.add_response(['warm'], "The pleasant warmth of the fire feels great!")
    fire.move_to(inn, True)

    hearth = scenery.Scenery('hearth', 'huge stone hearth', "This huge but otherwise unremarkable "
        "stone hearth is large enough for several patrons to crowd around and warm themselves on "
        "cold days.", unlisted=True)
    hearth.add_adjectives('huge', 'stone')
    hearth.move_to(inn, True)
    
    bar = scenery.Scenery('bar', 'long cherry bar', "Running the length of the long tavern is a "
        "polished cherrywood bar lined with simple wooden stools.", unlisted=True)
    bar.add_adjectives('long', 'cherry')
    bar.move_to(inn, True)

    stools = scenery.Scenery('stool', 'wooden stool', "The bar is lined with simple wooden stools "
        "that provide a comfortable seat for patrons to while away the hours.", unlisted=True)
    stools.add_adjectives('wooden', 'simple')
    stools.add_names('stool')
    stools.add_response(['sit'], "You take a seat briefly, and find the stool quite comfortable.")
    stools.move_to(inn, True)

    innkeeper = gametools.clone('domains.centrata.village.innkeeper')
    innkeeper.move_to(inn)
    return inn