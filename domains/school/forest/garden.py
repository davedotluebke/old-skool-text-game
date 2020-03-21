import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    garden = room.Room("garden", roomPath)
    garden.set_description("beautiful garden","This is a very beautiful garden in the northwest corner of Firefile Sorcery School that has many useful plants growing in it. A road leads off to the northwest.")
    garden.add_exit("south","domains.school.forest.field")
    garden.add_exit("southeast", "domains.school.school.grand_entry")
    garden.add_exit("west", "domains.school.forest.pine_forest")
    garden.add_exit("northwest", 'domains.school.forest.forest_road')

    sunflower = gametools.clone('domains.school.forest.sunflower')
    garden.insert(sunflower)

    poppy = gametools.clone('domains.school.forest.poppy')
    garden.insert(poppy)

    return garden

