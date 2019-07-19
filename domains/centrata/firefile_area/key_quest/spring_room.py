import gametools
import room

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('room', roomPath, indoor=True)
    r.set_description('old office', 'This office clearly belong to someone important but it has seen many years without use. The faded yellow paint is peelling off the walls.')
    r.add_adjectives('old',"important")
    r.add_exit('southwest', "domains.school.school.hallway")

    spring = gametools.clone('domains.centrata.firefile_area.key_quest.spring')
    r.insert(spring)

    return r