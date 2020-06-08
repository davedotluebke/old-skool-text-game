import creature

class Swallow(creature.NPC):
    def __init__(self):
        super().__init__("swallow", __file__, aggressive=1, movement=1)
        self.set_description("barn swallow", "This is a blue and orange barn swallow. It seems completely average.")
        self.add_adjectives("barn", "blue", "orange", "average")
    
    def move_around(self):
        possible_exits = list(self.location.exits)
        if self.location.id == "domains.school.elementQuest.portrait_gallery":
            possible_exits.append("domains.school.elementQuest.secret_lookout")
        return super().move_around()

def clone():
    return Swallow()
