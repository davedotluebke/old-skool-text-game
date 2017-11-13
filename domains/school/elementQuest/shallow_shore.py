import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    shallow_shore = lake_room.LakeRoom_underwater('shallow shore', roomPath, 'domains.school.elementQuest.lake_sw')
    shallow_shore.set_description('shallow shore', 'You find yourself in a shallow shoreline of the lake. The ground is covered with fine sand, and there are a few fish. You see something dark to the north but are not sure what it is.')
    shallow_shore.add_exit('north', 'domains.school.elementQuest.statue')
    shallow_shore.add_exit('east', 'domains.school.elementQuest.rusty_can')
    
    fish = gametools.clone('domains.school.elementQuest.fish')
    fish.move_to(shallow_shore)
    
    return shallow_shore