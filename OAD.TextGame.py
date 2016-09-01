import debug

from thing import Thing
from container import Container
from room import Room  
from creature import Creature 
from player import Player
from console import Console

class Game():
    """The Game class contains a console and associated game state (e.g. player object for the console).
    
    Eventually this will grow to include a list of players, associated consoles, etc."""
    def __init__(self):
        self.cons = Console()
        self.user = Player("testplayer")
        self.user.set_description('joe test', 'our test player named joe')
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)
        self.cons.set_user(self.user)

## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state and must be referenced by all the various objects. 
## 
game = Game()

bedroom = Room('bedroom')
hallway = Room('hallway')
kitchen = Room('kitchen')
entryway = Room('entryway')
woods = Room('woods')

bedroom.set_description('a dusty bedroom', 'The bare board walls of this bedroom are dusty. A musty smell fills the air.')
hallway.set_description('a dusty hallway', 'This hallway has dusty walls made of wood. It is dim.')
kitchen.set_description('a dusty kitchen with 50-year old apliences and decorations', 'This kitchen looks about 50 years old, and is very dusty but apears still useable.')
entryway.set_description('a barren entryway', 'The dusty entryway has one chandelier hanging from the celing.')
woods.set_description('some bright and cheerful woods', 'Theese woods have happy birdsongs and pretty trees. They are bright.')

woods.add_exit('west', entryway)
entryway.add_exit('east', woods)
entryway.add_exit('southwest', kitchen)
entryway.add_exit('south', hallway)
hallway.add_exit('north', entryway)
hallway.add_exit('northwest', kitchen)
hallway.add_exit('southeast', bedroom)
bedroom.add_exit('northwest', hallway)
kitchen.add_exit('northeast', entryway)
kitchen.add_exit('southeast', hallway)

bed = Thing('bed')
bed.set_description('a queen-size bed', 'A plain and simple queen-size bed.')
bed.set_weight(150000)
bed.set_volume(6000)
bedroom.insert(bed)

bag = Container('bag')
bag.set_description('a normal bag', 'A normal-looking brown bag.')
bag.set_weight(100)
bag.set_volume(10)
bag.set_max_weight_carried(20000)
bag.set_max_volume_carried(10)
woods.insert(bag)

plate = Thing('plate')
plate.set_description('a dinner plate', 'This is a normal-looking white dinner plate.')
plate.set_weight(1000)
plate.set_volume(1.25)
kitchen.insert(plate)

woods.insert(game.user)
game.cons.loop(game.user)
