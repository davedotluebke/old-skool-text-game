import gametools
import room
import scenery
import home.scott.house.exit_door as exit_door

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    mjs_office = room.Room('office', safe=True, indoor=True, pref_id=roomPath)
    mjs_office.set_description('medium-sized office', "This is a medium-sized office. There is a large black desk in "
    "the middle of it. Behind the desk you notice a small rolling chair and a bookcase. The bookcase stands partially "
    "in front of a mysterious door to the south. In front of the desk you see two blue fabric chairs facing it and a small end table. "
    "The office has two large windows, and a door to the west. ")

    mj_door = exit_door.Door('door', 'plain white door', 'This plain white door is on the west side of the room. ',
    'domains.renaissance_school.lobby', 'west', 'everyone')
    mj_door.add_adjectives('plain', 'white', 'mj', 'mjs', 'mj\'s')
    mj_door.move_to(mjs_office, True)

    strange_door = exit_door.Door('door', 'mysterious door', "This mysterious door is partially blocked by the bookcase. ",
    "domains.school.forest.hallway", "south", "everyone")
    strange_door.add_adjectives("mysterious", "strange", "partially", "blocked")
    strange_door.move_to(mjs_office, True)

    window1 = exit_door.Window("window", "large window", "This is a large but old window, with wavy glass.", "domains.centrata.village.north_village")
    window1.add_adjectives("large", "old", "glass", "wavy")
    window1.move_to(mjs_office, True)

    window2 = exit_door.Window("window", "large window", "This is a large but old window, with wavy glass.", "domains.centrata.village.back_street")
    window2.add_adjectives("large", "old", "glass", "wavy")
    window2.move_to(mjs_office, True)

    desk = gametools.clone("domains.renaissance_school.mjs_desk")
    desk.move_to(mjs_office)

    rolling_chair = scenery.Scenery('chair', 'rolling chair', 'This is a rolling chair behind the desk.', unlisted=True)
    rolling_chair.add_adjectives('rolling', 'desk')
    rolling_chair.add_response(['sit'], 'You sit in the chair.')
    rolling_chair.add_response(['stand'], 'You stand up.', False, True)
    rolling_chair.move_to(mjs_office, True)

    blue_chair1 = scenery.Scenery('chair', 'blue fabric chair', 'This is a blue fabric chair facing the desk.', unlisted=True)
    blue_chair1.add_adjectives('blue', 'fabric')
    blue_chair1.add_response(['sit'], 'You sit in the chair.')
    blue_chair1.add_response(['stand'], 'You stand up.', False, True)
    blue_chair1.move_to(mjs_office, True)

    blue_chair2 = scenery.Scenery('chair', 'blue fabric chair', 'This is a blue fabric chair facing the desk.', unlisted=True)
    blue_chair2.add_adjectives('blue', 'fabric')
    blue_chair2.add_response(['sit'], 'You sit in the chair.')
    blue_chair2.add_response(['stand'], 'You stand up.', False, True)
    blue_chair2.move_to(mjs_office, True)

    end_table = gametools.clone("domains.renaissance_school.mj_end_table")
    end_table.move_to(mjs_office, True)

    bookcase = gametools.clone("domains.renaissance_school.mj_bookcase")
    bookcase.move_to(mjs_office, True)
    
    return mjs_office
