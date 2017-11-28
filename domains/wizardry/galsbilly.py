from room import Room
from scenery import Scenery
from container import Container
from domains.school.transporter import TransportRoom
from domains.wizardry.deep_pocket import DeepPocketSignUpWizard
from domains.wizardry.gems import *

central_fountain = Room('square', safe=True)
government_entrences = Room('cobbled street', safe=True)
south_shopping_one = Room('shopping', safe=True)
restraunt_one = Room('gathernia', safe=True)

wizardry_transporter = TransportRoom('learn wizardry', central_fountain)

central_fountain.set_description('central square', 'This is a central square at the intersection of two major roads. You see stores to the south, government buildings to the north, houses to the east, and a sign for a wizardry school to the west.')
government_entrences.set_description('cobbled street', 'This is a cobbled street with many government buildings on the side. There are many doors to a variety of buildings. To the south you see the central fountain, while to the north the street continues.')
south_shopping_one.set_description('street covered with shops', 'This is a street covered with shops on two stories--ground floor and the floor above. To get to the higher shops you must fly, which is made possible by the sapphires you see mounted in the roadway. A restaurant called "Gathernia" catches your eye.') #TODO: Auto generate more shops (like books on the bookshelf)
restraunt_one.set_description('busy restaurant named Gathernia', 'This is a busy restaurant named "Gathernia". Here you see many people eating and talking.')

central_fountain.add_exit('north', government_entrences.id)
central_fountain.add_exit('south', south_shopping_one.id)
government_entrences.add_exit('south', central_fountain.id)
south_shopping_one.add_exit('north', central_fountain.id)
restraunt_one.add_exit('out', south_shopping_one.id)

south_shopping_one.add_enter('gathernia', restraunt_one.id)

central_fountain.add_adjectives('busy', 'central')
government_entrences.add_adjectives('dark', 'cobbled')
south_shopping_one.add_adjectives('lively', 'bright', 'busy')

government_entrences.add_names('street')

fountain = Scenery('fountain', 'crystal clear fountain', 'This is studded with gems in the center. All of the water coming out of the fountain is crystal clear.')
fountain.add_adjectives('gem-studded', 'crystal','clear')
fountain.move_to(central_fountain)

silemon = DeepPocketSignUpWizard(government_entrences)
silemon.move_to(government_entrences)

for i in range(1, 6):
    table = Container('table')
    table.set_description("wooden table numbered %s" % i, "This is a slightly battered wooden table at the restraunt. It has a number %s on it." % i)
    table.fix_in_place("The table is too heavy and awkward to move.")
    table.add_adjectives("wooden", "battered", "%s" % i, "table", "numbered")
    table.add_names("%s" % i)
    table.set_prepositions("on", "onto")
    table.set_max_volume_carried(5000)
    table.set_max_weight_carried(150000)
    restraunt_one.insert(table)

test_r = Ruby('ruby', 'normal ruby', 'This is a normal red ruby.')
test_r.move_to(central_fountain)

test_d = Diamond('diamond', 'normal diamond', 'This is a normal diamond.')
test_d.move_to(central_fountain)

test_o = Opal('opal', 'normal opal', 'This is a normal opal.')
test_o.move_to(central_fountain)

#TODO: Fix jade
#test_j = Jade('jade', 'rare jade', 'This is a rare jade. It is orange.')
#test_j.move_to(central_fountain)

    def enter(self, p, cons, oDO, oIDO):
        words = p.words
        del words[0]
        words = words
        sEnter = ''
        b = False
        for i in words:
            if b:
                sEnter += ' '
            sEnter += i.lower()
            b = True
        if sEnter in list(self.enters):
            dest = Thing.ID_dict[self.enters[sEnter]]
            if cons.user.move_to(dest):
                loc = cons.user.location
                cons.write("You enter %s" % sEnter.capitalize())
                self.emit("&nD%s enters %s" % (cons.user.id, sEnter.capitalize()))
                loc.report_arrival(cons.user)
                return True
            else:
                return "For some reason you are unable to enter %s." % sEnter.capitalize()
        else:
            return "I don't see anywhere named %s you can enter!" % sEnter.capitalize()


