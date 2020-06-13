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
        hidden_door = doors_and_windows.Door('door', 'hidden door', 'This is a hidden door carved into the west wall. A gentle breeze passes through the cracks in it.', 'domains.school.elementQuest.secret_room', 'west', [])
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
    r.set_description('airy portrait gallery', 'You find yourself in a airy circler room. The walls are lined with many differnt portraits of birds.'
    ' There is a plaque on the north wall and a door to the east. On the edge of the room, against the wall some wooden stairs lead up to the next level.'
    ' The floor is made of smooth stone and well polished.')
    r.add_adjectives('windy')
    r.add_exit('up', 'domains.school.elementQuest.armor_museum')
    r.add_exit('down', 'domains.school.elementQuest.statue_room')



    dark_portrait = scenery.Scenery ('portrait', 'dark portrait', 'This portrait depicts a great horned out on a hunt in the dark of night. It is painted in oil paint. You feel and tingling go up your spine.')
    dark_portrait.add_names('portrait', 'painting')
    dark_portrait.add_adjectives('dark', 'owl', 'night', 'oil', 'great horned')
    dark_portrait.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(dark_portrait)

    watercolor_portrait = scenery.Scenery ('portrait', 'watercolor portrait', 'This is a watercolor portrait. It depicts a eastern bluebird feeding its young on its nest in the branches of a beach tree. It makes you feel happy and hopefull.')
    watercolor_portrait.add_names('portrait', 'painting')
    watercolor_portrait.add_adjectives('light', 'bluebird', 'birdhouse', 'watercolor', 'water', 'color')
    watercolor_portrait.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(watercolor_portrait)

    pastel_portrait = scenery.Scenery ('portrait', 'pastel portrait', 'This is a vivid portrait that depicts a flock of parrots on a branch in the jungle. Its vividness stuns you.')
    pastel_portrait.add_names('portrait', 'painting')
    pastel_portrait.add_adjectives('bright', 'parrot', 'jungle', 'pastel')
    pastel_portrait.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(pastel_portrait)

    ink_portrait = scenery.Scenery ('portrait', 'ink portrait', 'This is a simple and old ink wash portrait painted on a very old piece of a paper. It depicts a a humbingbird hovering above a cluster of irises. The paper\'s age impresses you.')
    ink_portrait.add_names('portrait', 'painting')
    ink_portrait.add_adjectives('simple', 'old', 'humbingbird', 'ink', 'inkwash')
    ink_portrait.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(ink_portrait)

    encaustic_portrait = scenery.Scenery ('portrait', 'encaustic portrait', 'This encaustic painting looks like it is the oldest in the gallery. It is painted on a large slab of wood. It is abstract and seems to show a sparrow holding a seed in it\' mouth. Its abstractness intrest you.')
    encaustic_portrait.add_names('portrait', 'painting')
    encaustic_portrait.add_adjectives('abstract', 'old', 'sparrow', 'encaustic', 'oldest', 'wood')
    encaustic_portrait.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(encaustic_portrait)

    acrylic_portrait = scenery.Scenery ('portrait', 'acrylic portrait', 'This is an large acrylic portrait of a tree swallow swooping low over a lake, an ant held firmly in its beak. It is so realistic you almost feel like it is real.')
    acrylic_portrait.add_names('portrait', 'painting')
    acrylic_portrait.add_adjectives('realistic', 'lake', 'swallow', 'acrylic')
    acrylic_portrait.add_response(['take','steal','touch'], 'As you start to reach out you notice the plaque which reminds you not to touch any of the paintings.')
    r.insert(acrylic_portrait)

    plaque = scenery.Scenery ('plaque', 'metal plaque on wall', 'This is a normal metal plaque on the wall, you can try "read" it.', unlisted=False)
    plaque.add_names('plaque')
    plaque.add_adjectives('metal', 'normal')
    plaque.add_response(['read'], 'The plaque reads: Please do not touch any of the paintings. \n No flash photography \n No food or drink in the gallery')
    r.insert(plaque)

    wall = scenery.Scenery('wall', 'wall', 'This stone wall raps around the room, there is a door to the east and a large crack in the west wall.', unlisted=True)
    wall.add_adjectives('stone', 'circular')
    wall.add_names('west')
    r.insert(wall)

    crack = scenery.Scenery('crack', 'large crack', 'This is a large crack it is located in the west section of the wall right above the acrylic painting. In the crack you notice a hidden lever.', unlisted=True)
    crack.add_adjectives('large')
    crack.add_names('crack', 'crevice')
    r.insert(crack)

    l = Lever()
    r.insert(l)

    east_door = doors_and_windows.Door('door', 'wood door', 'This is a boring wooden door, it leads to the east.', 'domains.school.elementQuest.sauna_hall', 'east', [])
    east_door.add_adjectives('wooden','normal','boring')
    r.insert(east_door)

    water_fountain = gametools.clone('domains.school.elementQuest.water_fountain')
    r.insert(water_fountain)

    return r
