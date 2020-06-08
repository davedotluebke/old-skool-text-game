import domains.school.elementQuest.lake_room as lake_room
import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    inflow = lake_room.LakeRoom_underwater('inflow', roomPath, 'domains.school.elementQuest.lake_se')
    inflow.set_description('stream inflow', 'Here, the bottom of the lake is covered with a thick mud. A stream gurgles into the lake from the southeast.')
    inflow.add_exit('west', 'domains.school.elementQuest.rusty_can')
    inflow.add_exit('north', 'domains.school.elementQuest.doorway')
    
    return inflow
