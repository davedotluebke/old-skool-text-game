import gametools
import scenery
import room
import domains.centrata.orc_quest.prairie as prairie

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    orc_camp = room.Room('camp', roomPath)
    orc_camp.set_description('orc camp', 'This is the orc camp, awaiting further description.')

    if prairie.connection_exists(prairie.orc_camp_x-1, prairie.orc_camp_y, 1, 0, prairie.exit_probability):
        orc_camp.add_exit('west', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x-1}&{prairie.orc_camp_y}')
    if prairie.connection_exists(prairie.orc_camp_x, prairie.orc_camp_y, 1, 0, prairie.exit_probability):
        orc_camp.add_exit('east', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x+1}&{prairie.orc_camp_y}')
    if prairie.connection_exists(prairie.orc_camp_x, prairie.orc_camp_y, 0, 1, prairie.exit_probability):
        orc_camp.add_exit('north', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x}&{prairie.orc_camp_y+1}')
    if prairie.connection_exists(prairie.orc_camp_x, prairie.orc_camp_y-1, 0, 1, prairie.exit_probability):
        orc_camp.add_exit('south', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x}&{prairie.orc_camp_y-1}')
    
    return orc_camp
