import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    central_railway_platform = room.Room('platform', roomPath, indoor=True)
    central_railway_platform.set_description('railway station platform', 'You stand on the platform of a railway station. There are tracks on both sides, with signs labelling the one to your west as track 2, and the one to your east as track 3.')
    central_railway_platform.add_adjectives('railway', 'station', 'central')
    
    central_railway_platform.add_exit('south', 'domains.covtle.mangátle.railway_station_great_hall')

    return central_railway_platform
