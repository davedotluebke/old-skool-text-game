from debug import dbg

from thing import Thing
from container import Container
from room import Room  
from creature import Creature 
from creature import NPC
from player import Player
from console import Console
from bookcase import Bookcase
from scenery import Scenery
from sink import Sink

class Game():
    """The Game class contains a console and associated game state (e.g. player object for the console).
    
    Eventually this will grow to include a list of players, associated consoles, etc."""
    def __init__(self):
        self.cons = Console()
        self.user = Player("testplayer", self.cons)
        self.user.set_description('joe test', 'our test player named joe')
        self.user.set_max_weight_carried(750000)
        self.user.set_max_volume_carried(2000)
        self.cons.set_user(self.user)
        self.heartbeat_users = []

    def register_heartbeat(self, obj):
        """Add the specified object (obj) to the heartbeat_users list"""
        self.heartbeat_users.append(obj)
    
    def beat(self):
        """call all of the registered heartbeat functions"""
        for h in self.heartbeat_users:
            h.heartbeat()

    def loop(self):
        while True:
            self.beat()
            cmd = input('-> ')
            stop_going = self.cons.parser.parse(self.user, self.cons, cmd)
            if stop_going:
                dbg.shut_down()
                break

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
hideout = Room('secret hideout')
forest_one = Room('forest1')
forest_two = Room('forest2')
field = Room('field')
shack = Room('shack')

bedroom.set_description('a dusty bedroom', 'The bare board walls of this bedroom are dusty. A musty smell fills the air.')
hallway.set_description('a dusty hallway', 'This hallway has dusty walls made of wood. It is dim.')
kitchen.set_description('a dusty kitchen with 50-year old apliences and decorations', 'This kitchen looks about 50 years old, and is very dusty but apears still useable.')
entryway.set_description('a barren entryway', 'The dusty entryway has one chandelier hanging from the celing.')
woods.set_description('some bright and cheerful woods', 'Theese woods have happy birdsongs and pretty trees. They are bright.')
hideout.set_description('a secret room in the house', 'This is a secret hideout which is hard to find an entrence to but has magical exit doors.')
forest_one.set_description('a nice forest (ID = forest_one)', 'This is an ancient forest with towering trees. They must be hundreds of years old at least. (ID = forest_one)')
forest_two.set_description('a nice forest (ID = forest_two)', 'This is an ancient forest with towering trees. They must be hundreds of years old at least. (ID = forest_two)')
field.set_description('a field with a small shack on the west side', 'This field is on the outskirts of Firlefile sorcery school and has a small shack on the west side.')
shack.set_description('an empty shack', 'This shack appears to be abandoned and has nothing but cobwebs and walls.')

woods.add_exit('west', entryway)
woods.add_exit('north', forest_one)
entryway.add_exit('east', woods)
entryway.add_exit('southwest', kitchen)
entryway.add_exit('south', hallway)
hallway.add_exit('north', entryway)
hallway.add_exit('northwest', kitchen)
hallway.add_exit('southeast', bedroom)
bedroom.add_exit('northwest', hallway)
kitchen.add_exit('northeast', entryway)
kitchen.add_exit('southeast', hallway)
hideout.add_exit('south', bedroom)
hideout.add_exit('west', kitchen)
hideout.add_exit('up', woods)
forest_one.add_exit('south', woods)
forest_one.add_exit('east', forest_two)
forest_two.add_exit('west', forest_one)
forest_two.add_exit('east', field)
field.add_exit('west', forest_two)
field.add_exit('in', shack)
shack.add_exit('out', field)

bed = Thing('bed')
bed.set_description('a queen-size bed', 'A plain and simple queen-size bed.')
bed.set_weight(150000)
bed.set_volume(6000)
bedroom.insert(bed)

bookcase = Bookcase('bookcase', hideout)
entryway.insert(bookcase)

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

bird = NPC('bird', game)
bird.set_description('a bluebird', 'A nice looking little bluebird.')
bird.set_weight(200)
bird.set_volume(0.2)
bird.add_script('''Tweet!''')
bird.add_script('''Tweet tweet''')
bird.add_script(
'''Tweet tweet tweet,
tweet tweet
tweet, tweet,
Tweety tweet-tweet''')
woods.insert(bird)
bird.act_frequency = 1

butterfly = NPC('butterfly', game)
butterfly.set_description('a butterfly', 'A pretty monarch butterfly')
butterfly.add_script('''wh''')
field.insert(butterfly)

elm = Scenery("elm", "a massive old elm tree", "This huge elm tree must be over a hundred years old. You are tempted to hug it.", 
[(["hug", "hold"], "You give the old elm tree a long hug, and feel deeply satisfied.")])
elm.add_names("tree")
elm.add_adjectives("big", "massive", "old", "elm")
elm.add_response(["climb"], "The trunk is too broad to wrap your arms around, and the lowest branches are far too high to reach.")
woods.insert(elm)

beech = Scenery("beech", "an old beech tree full of carvings", 
"This large old beech tree has been scarred with the reminders of many passers-by, who decided to immortalize their visit by carving their initials into the tree.")
beech.add_names("tree")
beech.add_adjectives("old", "beech", "carved")
beech.add_response(["carve"], "You think about carving your own initials into the tree, but an uneasy feeling--as if the forest itself is watching--makes you stop.")
woods.insert(beech)

cabnets = Scenery('cabnets', 'a bunch of cabnets', 'The lightly stained wooden cabnets in this kitchen are slightly dusty.',
[(['open'], 'They are all empty.')])
kitchen.insert(cabnets)

sink = Sink('sink')
kitchen.insert(sink)

scarf = Thing('scarf')
scarf.set_description('a bright pink scarf', 'This bright pink scarf is very clean and soft.')
scarf.set_weight(200)
scarf.set_volume(0.1)
forest_one.insert(scarf)

bottle = Container('bottle')
bottle.set_description('a blue bottle', 'This blue bottle looks like a normal plastic bottle. It is unlabled.')
bottle.set_max_weight_carried(4e9)
bottle.set_max_volume_carried(3e9)
kitchen.insert(bottle)

woods.insert(game.user)
game.loop()
