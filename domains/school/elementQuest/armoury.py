import room
import gametools
import scenery


def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    r = room.Room('armoury', roomPath)
    r.set_description('armoury', 'This is a very small armoury with three armour stands in it.')
    r.add_exit('west', 'domains.school.elementQuest.armor_museum')

    chain_mail = gametools.clone('domains.school.elementQuest.chain_mail')

    return r
