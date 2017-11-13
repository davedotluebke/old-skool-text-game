import room

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    peninsula = room.Room('peninsula', roomPath)
    peninsula.set_description('small peninsula', 'This is a small peninsula which sticks out into the lake. The only ways to get here would be by swimming over the lake or by entering through the door to the southwest.')
    peninsula.add_exit('southwest', 'domains.school.elementQuest.path_choice')
    peninsula.add_exit('northeast', 'domains.school.elementQuest.lake_sw')
