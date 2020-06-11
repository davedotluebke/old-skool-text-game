import creature
import random

class Swallow(creature.NPC):
    def __init__(self):
        super().__init__("swallow", __file__, aggressive=1, movement=1)
        self.set_description("barn swallow", "This is a blue and orange barn swallow. It seems completely average.")
        self.add_adjectives("barn", "blue", "orange", "average")
        self.route = {
            'domains.school.elementQuest.balcony': True,
            'domains.school.elementQuest.bedroom': False,
            'domains.school.elementQuest.armor_museum': False,
            'domains.school.elementQuest.portrait_gallery': False,
            'domains.school.elementQuest.secret_room': False
        }
        self.set_spawn_interval(10)
        self.set_spawn_message('A swallow arrives.')
    
    def move_around(self):
        possible_exits = self.location.exits.copy()
        if self.location.id == "domains.school.elementQuest.portrait_gallery":
            possible_exits['west'] = "domains.school.elementQuest.secret_lookout"
        weights = []
        for i in possible_exits:
            if i in list(self.route) and not self.route[i]:
                weights.append(4)
            else:
                weights.append(0)
        direction = random.choices(list(possible_exits), weights=weights, k=1)[0]
        if direction in list(self.route) and not self.route[direction]:
            self.route[direction] = True
        return super().move_around(exit_list=possible_exits, direction=direction)

def clone():
    return Swallow()
