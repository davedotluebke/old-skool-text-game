import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    great_hall = room.Room('hall', roomPath, indoor=True)
    great_hall.set_description('railway station great hall', 'You stand in the great hall of Mangátle railway station, clearly labelled on a large sign above the large set of doors to the south. A ticket sales booth fills the centre. To the west there is a newsstand, to the east there is a café, and to the north the platforms begin.')
    great_hall.add_adjectives('great', 'main', 'railway', 'station')
    
    great_hall.add_exit('northwest', 'domains.covtle.mangátle.west_railway_platform')
    great_hall.add_exit('north', 'domains.covtle.mangátle.central_railway_platform')
    great_hall.add_exit('northeast', 'domains.covtle.mangátle.east_railway_platform')
    great_hall.add_exit('west', 'domains.covtle.mangátle.railway_station_newsstand')
    great_hall.add_exit('east', 'domains.covtle.mangátle.railway_station_café')
    great_hall.add_exit('south', 'domains.covtle.mangátle.calcí_at_railway_station')

    ticket_sales_booth = scenery.Scenery('booth', 'ticket sales booth', 'This is a booth labelled Tevaðon Adcovtle, with ticket prices labelled on a large chalkboard above the sales area. Nobody is currently in the booth.')
    ticket_sales_booth.add_adjectives('ticket', 'sales')
    ticket_sales_booth.add_response(['enter'], 'As if anticipating people like you, the door into ticket sales booth is locked.')
    ticket_sales_booth.move_to(great_hall, True)

    large_sign = scenery.Scenery('sign', 'large sign', 'This massive sign with a clock stands above the doors to the south. At the top it reads "Mangátle" in large letters. Below that, the schedule for the day is listed in removable letters, to the right of a very large clock.')
    large_sign.add_adjectives('large', 'massive')
    large_sign.add_response(['change', 'alter'], 'It is far too high to reach.')
    large_sign.move_to(great_hall, True)

    return great_hall
