import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    east_railway_platform = room.Room('platform', roomPath, indoor=True)
    east_railway_platform.set_description('railway station platform', 'You stand on the platform of a railway station. To the east there is a stone wall, signed along the platform with signs reading "Mangátle", while to the west there is a track, labelled above as track 4.')
    east_railway_platform.add_adjectives('railway', 'station', 'east')
    
    east_railway_platform.add_exit('south', 'domains.covlte.mangátle.railway_station_great_hall')

    return east_railway_platform
