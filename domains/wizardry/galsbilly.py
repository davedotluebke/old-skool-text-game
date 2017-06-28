from room import Room
from transporter import TransportRoom
from scenery import Scenery

central_fountain = Room('square')
government_entrences = Room('cobbled street')
south_shopping_one = Room('shopping')

wizardry_transporter = TransportRoom('learn wizardry', central_fountain)

central_fountain.set_description('central square', 'This is a central square at the intersection of two major roads. You see stores to the south, government buildings to the north, houses to the east, and a sign for a wizardry school to the west.')
government_entrences.set_description('cobbled street', 'This is a cobbled street with many government buildings on the side. There are many doors to a variety of buildings. To the south you see the central fountain, to the north the street continues.')
south_shopping_one.set_description('street covered with shops', 'This is a street covered with shops on two stories - ground floor and the floor above. To get to the higher shops you must fly, which can be done because of saphires you see mounted in the roadway. A restraunt called "Gathernia" catches your eye.') #TODO: Auto generate more shops (like books on the bookshelf)

central_fountain.add_exit('north', government_entrences)
government_entrences.add_exit('south', central_fountain)

central_fountain.add_adjectives('busy', 'central')
government_entrences.add_adjectives('dark', 'cobbled')

government_entrences.add_names('street')

fountain = Scenery('fountain', 'crystal clear fountain', 'This is studded with gems in the center. All of the water coming out of the fountain is crystal clear.')
fountain.add_adjectives('gem-studded', 'crystal','clear')
fountain.move_to(central_fountain)
