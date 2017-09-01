import room
import gametools
import scenery

class FireQuestPotionRoom(room.Room):
    def take(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO == 'flask':
            l = self.contents[:]
            for i in l:
                if i.path == 'domains.school.elementQuest.flask':
                    cons.write('You decide not to be greedy, as you already have a flask.')
                    return True
                if i.contents:
                    l += i.contents

            f = gametools.clone('domains.school.elementQuest.flask')
            if cons.user.insert(f):
                return "You fail to take a flask from the shelf."
            cons.write('You take a flask from the shelf.')
            self.emit('%s takes a flask from the open shelf.' % cons.user.names[0], [cons.user])
            return True
        return super().take(p, cons, oDO, oIDO)

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = FireQuestPotionRoom('potion room', roomPath)
    r.indoor = True
    r.set_description('potion room', 'This room has shelves along the walls. '
    'On the shelves there are many flasks. In the center of the room sits an enormous cauldron.')
    r.add_exit('northeast', 'domains.school.elementQuest.shaft_of_sunlight')

    cauldron = gametools.clone('domains.school.elementQuest.cauldron')
    r.insert(cauldron)
    return r
