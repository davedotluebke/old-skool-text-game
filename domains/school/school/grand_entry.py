import gametools
import room
import scenery

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    # Room does not yet exist, create it

    grand_entry = room.Room('grand entry', safe=True, pref_id=roomPath)
    grand_entry.indoor = True
    grand_entry.set_description('grand school entryway', 'This is the most magnificent entryway you have ever seen. The enormous front door is at the top of the marble staircase, with huge pillars on either side.')
    grand_entry.add_names('entry', 'entryway')
    grand_entry.add_adjectives('grand', 'magnificent')
    grand_entry.add_exit('southwest', 'domains.school.forest.field')
    grand_entry.add_exit('northwest', 'domains.school.forest.garden')
    grand_entry.add_exit('east', 'domains.school.school.great_hall')

    pillar = scenery.Scenery('pillar', 'huge pillar', 'This huge fluted pillar has ionic capitals.', unlisted=True)
    pillar.add_adjectives('huge', 'fluted', 'ionic')
    pillar.add_names('pillars')
    pillar.move_to(grand_entry, True)
    
    return grand_entry
