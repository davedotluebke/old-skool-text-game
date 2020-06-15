import creature
import random

class Swallow(creature.NPC):
    def __init__(self):
        super().__init__("swallow", __file__, aggressive=0, movement=1)
        self.act_frequency = 1
        self.set_description("barn swallow", "This is a blue and orange barn swallow. It seems completely average.")
        self.add_adjectives("barn", "blue", "orange", "average")
        self.route = {
            'domains.school.elementQuest.balcony': True,
            'domains.school.elementQuest.bedroom': False,
            'domains.school.elementQuest.armor_museum': False,
            'domains.school.elementQuest.portrait_gallery': False,
            'domains.school.elementQuest.secret_room': False
        }
        self.set_spawn_interval(30)
        self.set_spawn_message('A swallow arrives.')
    
    def move_around(self):
        if not self.location.exits:
            return
        possible_exits = self.location.exits.copy()
        if self.location.id == "domains.school.elementQuest.portrait_gallery":
            possible_exits['west'] = "domains.school.elementQuest.secret_room"
        if self.location.id == "domains.school.elementQuest.secret_room":
            self.emit("The swallow flies away at a very average speed.")
            self.destroy()
            return
        weights = []
        for i in possible_exits:
            if possible_exits[i] in list(self.route) and not self.route[possible_exits[i]]:
                weights.append(6)
            else:
                weights.append(1)
        direction = random.choices(list(possible_exits), weights=weights, k=1)[0]
        if possible_exits[direction] in list(self.route):
            self.route[possible_exits[direction]] = True
        return super().move_around(exit_list=possible_exits, direction=direction)

def clone():
    return Swallow()
