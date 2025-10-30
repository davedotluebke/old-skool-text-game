import gametools
import scenery
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    newsstand = room.Room('newsstand', roomPath, indoor=True)
    newsstand.set_description('railway station newsstand', 'This newsstand is on the west side of the railway station. A stone desk stands on the south side of the newsstand. On the north side, there is a selection of newspapers, magazines, and books for sale on a shelf.')
    newsstand.add_adjectives('railway', 'station', 'news')
    newsstand.add_names('stand')
    newsstand.add_exit('east', 'domains.covtle.mangátle.railway_station_great_hall')

    news_agent = gametools.clone('domains.covtle.mangátle.railway_station_news_agent')
    news_agent.move_to(newsstand, True)

    newsstand_shelf = gametools.clone('domains.covtle.mangátle.newsstand_shelf')
    newsstand_shelf.move_to(newsstand, True)

    return newsstand
