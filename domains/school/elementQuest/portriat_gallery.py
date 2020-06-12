import room
import gametools
import thing
import scenery
import doors_and_windows

class Lever(scenery.Scenery):
    def __init__(self):
        super().__init__('lever', 'hidden lever', 'This lever is hidden in a large crack in the wall', unlisted = True)
        self.door = None

    def pull(self, p, cons, oDO, oIDO):
        if oDO != self:
            return 'I don\'t see what you are trying to pull!'
        if self.door:
            cons.user.perceive('The door is already open!')
        cons.user.perceive('As you pull on the lever the room trembles and the painting of a tree swallow slides aside revealing a secret door carved into the west wall.')
        self.emit('&nD%s pulls on a hidden lever releaving a secret door to the west.')
        hidden_door = doors_and_windows.Door('door', 'hidden door', 'This is a hidden door carved into the west wall. A gentle breeze passes through the cracks in it.', 'domains.school.elementQuest.secret_lookout', 'west', [])
        hidden_door.add_adjectives('hidden', 'carved', 'cracked')
        cons.user.location.insert(hidden_door)
        self.door = hidden_door
        return True

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    r = room.Room('hall', roomPath)
    r.indoor = True
    r.set_description('airy portriat gallery', 'You find yourself in a airy circler room. The walls are lined with many differnt portriats of birds.'
    ' There is a plaque on the north wall and a door to the east. On the edge of the room, against the wall some wooden stairs lead up to the next level.'
    ' The floor is made of smooth stone and well polished.')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.armor_museum')
    r.add_exit('down', 'domains.school.elementQuest.statue_room')



    dark_portriat = scenery.Scenery ('portriat', 'dark portriat', 'This portriat depicts a great horned out on a hunt in the dark of night. It is painted in oil paint. You feel and tingling go up your spine.')
    dark_portriat.add_names('portriat', 'painting')
    dark_portriat.add_adjectives('dark', 'owl', 'night', 'oil', 'great horned')
    dark_portriat.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(dark_portriat)

    watercolor_portriat = scenery.Scenery ('portriat', 'watercolor portriat', 'This is a watercolor portriat. It depicts a eastern bluebird feeding its young on its nest in the branches of a beach tree. It makes you feel happy and hopefull.')
    watercolor_portriat.add_names('portriat', 'painting')
    watercolor_portriat.add_adjectives('light', 'bluebird', 'birdhouse', 'watercolor', 'water', 'color')
    watercolor_portriat.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(watercolor_portriat)

    pastel_portriat = scenery.Scenery ('portriat', 'pastel portriat', 'This is a vivid portriat that depicts a flock of parrots on a branch in the jungle. Its vividness stuns you.')
    pastel_portriat.add_names('portriat', 'painting')
    pastel_portriat.add_adjectives('bright', 'parrot', 'jungle', 'pastel')
    pastel_portriat.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(pastel_portriat)

    ink_portriat = scenery.Scenery ('portriat', 'ink portriat', 'This is a simple and old ink wash portriat painted on a very old piece of a paper. It depicts a a humbingbird hovering above a cluster of irises. The paper\'s age impresses you.')
    ink_portriat.add_names('portriat', 'painting')
    ink_portriat.add_adjectives('simple', 'old', 'humbingbird', 'ink', 'inkwash')
    ink_portriat.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(ink_portriat)

    encaustic_portriat = scenery.Scenery ('portriat', 'encaustic portriat', 'This encaustic painting looks like it is the oldest in the gallery. It is painted on a large slab of wood. It is abstract and seems to show a sparrow holding a seed in it\' mouth. Its abstractness intrest you.')
    encaustic_portriat.add_names('portriat', 'painting')
    encaustic_portriat.add_adjectives('abstract', 'old', 'sparrow', 'encaustic', 'oldest', 'wood')
    encaustic_portriat.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(encaustic_portriat)

    acrylic_portriat = scenery.Scenery ('portriat', 'acrylic portriat', 'This is an large acrylic portrait of a tree swallow swooping low over a lake, an ant held firmly in its beak. It is so realistic you almost feel like it is real.')
    acrylic_portriat.add_names('portriat', 'painting')
    acrylic_portriat.add_adjectives('realistic', 'lake', 'swallow', 'acrylic')
    acrylic_portriat.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(acrylic_portriat)

    plaque = scenery.Scenery ('plaque', 'metal plaque on wall', 'This is a normal metal plaque on the wall, you can try "read" it.', unlisted=False)
    plaque.add_names('plaque')
    plaque.add_adjectives('metal', 'normal')
    plaque.add_response(['read'], 'The plaque reads: Please do not touch any of the paintings. \n No flash photography \n No food or drink in the gallery')
    r.insert(plaque)

    wall = scenery.Scenery('wall', 'wall', 'This stone wall raps around the room, there is a door to the east and a large crack in the west wall.', unlisted=True)
    wall.add_names('wall')
    wall.add_adjectives('stone', 'circular')

    crack = scenery.Scenery('crack', 'large crack', 'This is a large crack it is located in the west section of the wall right above the acrylic painting. In the crack you notice a hidden lever.', unlisted=True)
    crack.add_adjectives('large')
    crack.add_names('crack', 'crevice')


    east_door = doors_and_windows.Door('door', 'wood door', 'This is a boring wooden dooor, it leads to the east.', 'domians.school.elementQuest.hall_to_sauna', 'east', [])
    east_door.add_adjectives('wooden','normal','boring')
    r.insert(east_door)

    water_fountain = gametools.clone('domains.school.elementQuest.water_fountain')
    r.insert(water_fountain)

    return r
