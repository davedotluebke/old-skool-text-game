import room
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    air_lounge = room.Room('lounge', roomPath, safe=True)
    air_lounge.set_description('high tower', 'This high tower feels as if it is nearly touching the sky. A black metal rail surrounds the tower, except to the south where a rainbow shines down on a stone bridge. The ground is covered in soft white pillows. There is an oak trapdoor in the centre of the tower.')
    air_lounge.add_exit('south', 'domains.school.school.air_bridge')
    return air_lounge
