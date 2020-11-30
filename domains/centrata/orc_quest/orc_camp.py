import gametools
import scenery
import room
import domains.centrata.orc_quest.prairie as prairie

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    orc_camp = room.Room('camp', roomPath)
    orc_camp.set_description('orc camp', "This can only be the camp of the orcs. The tall grass of "
        "the prairie here is trampled, scattered with trash, and smeared with unspeakable filth. A "
        "line of closely-spaced stakes forms a makeshift barrier, a pile of rotting furs serves as a "
        "crude bed, and a blackened firepit contains the charred remains of the orc's last  meal -- "
        "charred bones, still smoking.")
    furs = scenery.Scenery("furs", "pile of furs", "This pile of mangy furs and rotting hides is "
        "thrown on the ground to serve as a bed. The smell of orc is almost overpowering.", unlisted=True)
    furs.add_names("pile", "bed")
    furs.add_adjectives("rotting", "mangy", "crude")
    stakes = scenery.Scenery("stakes", "line of stakes", "A line of sharpened stakes have been driven "
        "into the ground to form a crude but effective barrier. There is just enough room to slide "
        "between the stakes, but they would certainly slow down attackers. Driven onto some of the "
        "stakes are heads of unfortunate creatures, in varying stages of decomposition.", unlisted=True)
    stakes.add_names("line", "barrier", "stake")
    stakes.add_adjectives("crude", "sharpened", "line of", "closely-spaced", "makeshift")
    bones = scenery.Scenery("bones", "charred bones", "These are the smoking bones of some large "
        "creature.  You try not to think about just what (or who) it was.", unlisted=True)    
    bones.add_names("bone")
    bones.add_adjectives("charred")
    
    orc_camp.insert(furs)
    orc_camp.insert(stakes)
    orc_camp.insert(bones)

    small1 = gametools.clone("domains.centrata.orc_quest.small_orc1")
    small2 = gametools.clone("domains.centrata.orc_quest.small_orc2")
    small3 = gametools.clone("domains.centrata.orc_quest.small_orc3")
    med1 = gametools.clone("domains.centrata.orc_quest.medium_orc1")
    med2 = gametools.clone("domains.centrata.orc_quest.medium_orc2")
    chief = gametools.clone("domains.centrata.orc_quest.chief_orc")
    orc_camp.insert(small1)
    orc_camp.insert(small2)
    orc_camp.insert(small3)
    orc_camp.insert(med1)
    orc_camp.insert(med2)
    orc_camp.insert(chief)
    
    if prairie.connection_exists(prairie.orc_camp_x-1, prairie.orc_camp_y, 1, 0, prairie.exit_probability):
        orc_camp.add_exit('west', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x-1}&{prairie.orc_camp_y}')
    if prairie.connection_exists(prairie.orc_camp_x, prairie.orc_camp_y, 1, 0, prairie.exit_probability):
        orc_camp.add_exit('east', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x+1}&{prairie.orc_camp_y}')
    if prairie.connection_exists(prairie.orc_camp_x, prairie.orc_camp_y, 0, 1, prairie.exit_probability):
        orc_camp.add_exit('north', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x}&{prairie.orc_camp_y+1}')
    if prairie.connection_exists(prairie.orc_camp_x, prairie.orc_camp_y-1, 0, 1, prairie.exit_probability):
        orc_camp.add_exit('south', f'domains.centrata.orc_quest.prairie?{prairie.orc_camp_x}&{prairie.orc_camp_y-1}')
    

    return orc_camp
