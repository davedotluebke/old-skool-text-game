from debug import dbg

from gameserver import Game
from action import Action
from thing import Thing
from container import Container
from room import Room  
from creature import Creature 
from creature import NPC
from player import Player
from console import Console
from scenery import Scenery
from liquid import Liquid
from weapon import Weapon
from armor import Armor

from bookcase import Bookcase
from sink import Sink
from cave import CaveEntry
from flashlight import Flashlight
from flower import Flower

## 
## "game" is a special global variable, an object of class Game that holds
## the actual game state. 
## 
game = Game()
nulspace = Room('nulspace')         #"nulspace" is a room for objects that should be deleted. TODO: Automaticly delete items from nulspace every heartbeat.

woods = Room('woods')
woods.set_description('bright and cheerful woods', 'Theese woods have happy birdsongs and pretty trees. They are bright.')

bedroom = Room('bedroom')
hallway = Room('hallway')
kitchen = Room('kitchen')
entryway = Room('entryway')
forest_one = Room('forest')
forest_two = Room('forest')
forest_three = Room('forest')
field = Room('field')
shack = Room('shack')
cave = Room('cave', light=0)
cave_entrance = CaveEntry('cave mouth', forest_three, game)
garden = Room("garden")

import school

bedroom.set_description('dusty bedroom', 'The bare board walls of this bedroom are dusty. A musty smell fills the air.')
hallway.set_description('dusty hallway', 'This hallway has dusty walls made of wood. It is dim.')
kitchen.set_description('dusty kitchen with 50-year old apliences and decorations', 'This kitchen looks about 50 years old, and is very dusty but apears still useable.')
entryway.set_description('barren entryway', 'The dusty entryway has one chandelier hanging from the celing.')
forest_one.set_description('nice forest', 'This is an ancient forest with towering trees. They must be hundreds of years old at least.')
forest_two.set_description('nice forest', 'This is an ancient forest with towering trees. They must be hundreds of years old at least.')
forest_three.set_description('ancient forest', 'This is an ancient forest with towering trees. They must be hundreds of years old at least. The trees seem gloomy here. There is a small dark cave to the west.')
field.set_description('field with a small shack on the west side', 'This field is on the outskirts of Firlefile sorcery school and has a small shack on the west side.')
shack.set_description('empty shack', 'This shack appears to be abandoned and has nothing but cobwebs and walls.')
cave.set_description('terrifying dark cave', 'This is one of the most scary caves you have ever been in. You are anxiousley looking around to see if there are any monsters.')
garden.set_description("beutiful garden","This is a very beautiful garden in the northwest corner of Firlefile Sorcery School, and has many useful plants growing in it.")

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
forest_one.add_exit('south', woods)
forest_one.add_exit('east', forest_two)
forest_two.add_exit('west', forest_one)
forest_two.add_exit('east', field)
forest_one.add_exit('northwest', forest_three)
forest_three.add_exit('southeast', forest_one)
forest_three.add_exit('west', cave_entrance)
cave.add_exit('east', forest_three)
field.add_exit('west', forest_two)
field.add_exit('in', shack)
field.add_exit("north",garden)
field.add_exit('northeast', Thing.ID_dict['grand entry'])
shack.add_exit('out', field)
cave_entrance.add_exit('east', forest_three)
cave_entrance.add_exit('in', cave)
garden.add_exit("south",field)
garden.add_exit('southeast', Thing.ID_dict['grand entry'])

forest_one.add_names('forest')
forest_one.add_adjectives('ancient','towering','nice')
forest_two.add_names('forest')
forest_two.add_adjectives('ancient','towering','nice')
forest_three.add_names('forest')
forest_three.add_adjectives('ancient','towering','gloomy')
cave.add_adjectives('scary', 'dark', 'terrifying')

bag = Container('bag')
bag.set_description('normal bag', 'A normal-looking brown bag.')
bag.set_weight(100)
bag.set_volume(10)
bag.set_max_weight_carried(20000)
bag.set_max_volume_carried(10)
bag.closable = True
woods.insert(bag)

flashlight = Flashlight('flashlight')
flashlight.set_description('old flashlight', 'An old metal flashlight.')
woods.insert(flashlight)

rake = Scenery("rake","broken rake", "This rake looks like it broke a long time ago.")
rake.add_adjectives("broken")
rake.add_response(["get","take"], "When you lean down to take it one of the tines pokes you in the eye. Ow! ")
rake.add_response(["rake", "use"],"You can not reach the handle.")
shack.insert(rake)

bed = Scenery('bed','decrepit old bed', 'This decrepit bed supports a bare stained mattress and is covered with a thick layer of dust.')
bed.add_adjectives('old', 'decrepit')
bed.add_response(['sleep'], 'You briefly consider sleeping on the dusty soiled mattress, and quickly think better of it.', True, True)
bed.add_response(['make'], 'You look around for sheets or blankets, but see nothing suitable with which to make the bed.')
bedroom.insert(bed)

oak = Scenery('oak', 'menacing old oak', 'This is an old oak that is leaning over the trail. It seems to be scowling at you. You are afraid.')
oak.add_adjectives('menacing', 'old', 'oak')
oak.add_names('tree')
oak.add_response(['climb'], "The towering oak looks climbable, but it is a menacing old tree, the most so you have ever seen, so you decide to look around for other trees.")
oak.add_response(['grab', 'hold', 'touch', 'hug'], "To touch the scary old tree for no reson seems silly, and slightly scary, so you decide not to. You think that if you saw a nice tree you would hug it.")
forest_three.insert(oak)

willow = Scenery('willow', 'sad weeping willow', 'This is the most mournful weeping willow you have ever seen. You almost cry from looking at it.')
willow.add_adjectives('weeping','sad','mournful','willow')
willow.add_names('tree')
willow.add_response(['climb'], 'You cannot hold onto the branches, and they are over a small river.',)
willow.add_response(['cry', 'weep'], 'You cry as you look at the willow, but then you see the menacing old oak tree across the path, and you eventually stop.', False, True)
willow.add_response(['hug', 'hold'], 'This just isn\'t the right tree to hug.')
forest_three.insert(willow)

bird = NPC('bird', game)
bird.set_description('bluebird', 'A nice looking little bluebird.')
bird.set_weight(200)
bird.set_volume(0.2)
bird.add_script("""Tweet!""")
bird.add_script("""Tweet tweet""")
bird.add_script(
"""Tweet tweet tweet,
tweet tweet
tweet, tweet,
Tweety tweet-tweet""")
woods.insert(bird)
bird.act_frequency = 1

seed = Thing('seed')
seed.set_description('sunflower seed','This is a normal sunflower seed that looks like it has been eaten.')
seed.location = bird
bird.insert(seed)

butterfly = NPC('butterfly', game)
butterfly.set_description('butterfly', 'A pretty monarch butterfly')
butterfly.add_script("""wh""")
field.insert(butterfly)

elm = Scenery("elm", "massive old elm tree", "This huge elm tree must be over a hundred years old. You are tempted to hug it.")
elm.add_names("tree")
elm.add_adjectives("big", "massive", "old", "elm")
elm.add_response(["hug", "hold"], "You give the old elm tree a long hug, and feel deeply satisfied.")
elm.add_response(["climb"], "The trunk is too broad to wrap your arms around, and the lowest branches are far too high to reach.")
forest_one.insert(elm)

beech = Scenery("beech", "old beech tree full of carvings", 
"This large old beech tree has been scarred with the reminders of many passers-by, who decided to immortalize their visit by carving their initials into the tree.")
beech.add_names("tree")
beech.add_adjectives("old", "beech", "carved")
beech.add_response(["carve"], "You think about carving your own initials into the tree, but an uneasy feeling--as if the forest itself is watching--makes you stop.")
woods.insert(beech)

pine_one = Scenery('pine', 'old sturdy pine tree','This pine tree has clearly been here for quite a while. It seems strong and has some low branches you think you can reach.')
pine_one.add_names('pine','tree')
pine_one.add_adjectives('old','sturdy','pine')
pine_one.add_response(['climb'], "Unfortunatley, the lower branches are not as strong as the sturdy trunk, and you can't seem to get a hold of the higher ones.")
forest_one.insert(pine_one)

pine_two = Scenery('pine', 'old sturdy pine tree','This pine tree has clearly been here for quite a while. It seems strong and has some low branches you think you can reach.')
pine_two.add_names('pine','tree')
pine_two.add_adjectives('old','sturdy',)
pine_two.add_response(['climb'], "Unfortunatley, the lower branches are not as strong as the sturdy trunk, and you can't seem to get a hold of the higher ones.")
forest_two.insert(pine_two)

scarf = Thing('scarf')
scarf.set_description('bright pink scarf', 'This bright pink scarf is very clean and soft.')
scarf.set_weight(200)
scarf.set_volume(0.1)
forest_one.insert(scarf)

sunflower = Flower("sunflower", 'sunflower')
sunflower.set_description("giant sunflower" , "By looking at this giant sunflower you start feeling more happy.")
sunflower.set_volume(3)
sunflower.set_weight(200)
sunflower.add_adjectives('happiness','giant')
sunflower.actions.append(Action(sunflower.take, ['pick'], True, False))
garden.insert(sunflower)

poppy = Flower("poppy", 'poppy')
poppy.set_description("red poppy","This poppy is VERY pretty! You really want to pick it!")
poppy.set_volume(2.122)
poppy.set_weight(200)
poppy.add_adjectives("very","pretty")
poppy.actions.append(Action(poppy.take, ['pick'], True, False))
garden.insert(poppy)

tomato_plant = Container("tomato plant")
tomato_plant.set_description("tomato plant","This tomato plant look like it prodoces yummy tomatoes.")      #CLEANUP
#tomato_plant.

table = Container('table')
table.set_description("kitchen table", "This dated-looking kitchen table has chrome edging and a formica top.")
table.fix_in_place("The table is too heavy and awkward to move.")
table.add_adjectives("kitchen", "dated", "formica")
table.set_prepositions("on", "onto")
table.set_max_volume_carried(5000)
table.set_max_weight_carried(150000)
kitchen.insert(table)

plate = Thing('plate')
plate.set_description('dinner plate', 'This is a normal-looking white dinner plate.')
plate.set_weight(1000)
plate.set_volume(1.25)
plate.add_adjectives('dinner','white')
table.insert(plate)

bottle = Container('bottle')
bottle.set_description('blue bottle', 'This blue bottle looks like a normal plastic bottle. It is unlabled.')
bottle.add_adjectives('blue', 'plastic', 'unlabled')
bottle.set_max_weight_carried(4e9)
bottle.set_max_volume_carried(3e9)
bottle.liquid = True
table.insert(bottle)

gold = Thing('gold')
gold.set_description('bunch of shiny gold coins', 'This is a collection of seven shiny real gold coins.')
gold.set_weight(74000)
cave.insert(gold)

cabinets = Container('cabinets')
cabinets.set_description('bunch of cabinets', 'The lightly stained wooden cabinets in this kitchen are slightly dusty.')
cabinets.fix_in_place("How do you think you can take cabinets!? You can\'t.")
cabinets.add_names('cabinet')
cabinets.add_adjectives('wood', 'lightly stained','stained','old','1960s',"60's")
cabinets.set_max_volume_carried(5000)
cabinets.set_max_weight_carried(100000)
cabinets.plural = True
cabinets.closable = True
cabinets.close()
kitchen.insert(cabinets)

flask = Container('flask')
flask.set_description('small flask', 'This is a small flask of clear glass. ')
flask.add_adjectives('small', 'clear', 'glass')
flask.set_max_volume_carried(0.050)
flask.set_max_weight_carried(200)
flask.liquid = True

molasses = Liquid('molasses')
molasses.set_description('thick brown molasses', 'This brownish liquid is sweet and thick. Not surprisingly, it is used in recipes as a sweetener and a thickener.')
molasses.add_adjectives('thick', 'brown', 'brown', 'brownish')
molasses.set_volume(0.040)
molasses.set_weight(40)

flask.insert(molasses)
cabinets.insert(flask)

glass_bottle = Container('bottle')
glass_bottle.set_description("normal glass bottle","This is a normal glass bottle It looks quite usable.")

sink = Sink('sink')
sink.add_adjectives('metal', "60's")
kitchen.insert(sink)


# Begin experimental test code
monster = NPC('monster', game, 2)
monster.set_description('terrible monster', 'This is a horrible monster. You want to run away from it.')
monster.set_combat_vars(50, 60, 80, 40)
monster.act_frequency = 1
monster.set_volume(20)
monster.set_weight(500000)

sword = Weapon('sword', 6, 30, 2)
sword.set_description('rusty old sword', 'This is a rusty old sword the monster has for testing purposes.')

leather_suit = Armor('leather suit', 25, 2)
leather_suit.set_description('leather skin', 'A sturdy leather hide')

cave.insert(monster)
monster.insert(sword)
monster.insert(leather_suit)

game.user.hitpoints = 100
game.user.health = game.user.hitpoints
# End experimental test code


(Thing.ID_dict['great hall']).insert(game.user)
(Thing.ID_dict['scroll']).move_to(game.user)
game.user.start_loc = (Thing.ID_dict['great hall'])
game.user.cons.write("\nWelcome to Firlefile Sorcery School!\n\n"
"Type 'look' to examine your surroundings or an object, "
"'inventory' to see what you are carrying, " 
"'quit' to end the game, and 'help' for more information.")
game.loop()


