import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    café = room.Room('café', roomPath, indoor=True)
    café.set_description('small café', 'This small café offers a variety of dishes, including egg and cheese curds, beef and tomato stew, and mashed potatoes and melted cheese, plus a selection of baked goods.')
    café.add_adjectives('small')
    café.add_names('cafe')
    café.add_exit('west', 'domains.covtle.mangátle.railway_station_great_hall')

    # TODO: Add scenery and café salesperson

    return café
