import gametools
import doors_and_windows
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    west_railway_platform = room.Room('platform', roomPath, indoor=True)
    west_railway_platform.set_description('railway station platform', 'You stand on the platform of a railway station. To the west there is a stone wall, signed along the platform with signs reading "Mangátle", while to the east there is a track, labelled above as track 1.')
    west_railway_platform.add_adjectives('railway', 'station', 'west')
    
    west_railway_platform.add_exit('southeast', 'domains.covtle.mangátle.railway_station_great_hall')

    gilded_door = doors_and_windows.Door('door', 'gilded door', 'This is a gilded door with golden trim around an otherwise plain door.', 'home.johanna.house.er31795', 'west', ['johanna'])
    gilded_door.add_adjectives('gilded')
    gilded_door.move_to(west_railway_platform, True)

    return west_railway_platform
