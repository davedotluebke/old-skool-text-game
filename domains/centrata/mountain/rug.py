import thing
import action
import doors_and_windows

class Rug(thing.Thing):
    def __init__(self):
        super().__init__("rug", __file__)
        self.set_description("threadbare rug", "This rug is threadbare. It holds tints that suggest that it might have once been red, but it's hard to tell.")
        self.add_adjectives("red", "threadbare")
        self.add_names("carpet")
    
    def reveal_trapdoor(self, p, cons, oDO, oIDO):
        """Reveal the trapdoor, returning True if the trapdoor was sucessfully revealed and False if it was not."""
        if self.location.id == 'domains.centrata.mountain.hut' and not self.location.passage_revealed:
            cons.user.perceive("You move the rug, revealing a trapdoor in the floor!")
            self.location.emit("&nD%s moves the rug, revealing a trapdoor in the floor!" % cons.user.name(), ignore=[cons.user])
            trapdoor = doors_and_windows.Door("trapdoor", "trapdoor in the floor", "This heavy wooden trapdoor lies in the floor of the hut", "domains.centrata.mountain.cellar", "down", [])
            self.location.insert(trapdoor, True)
            self.location.set_description('stone hut', 'Between the solid stone walls this small hut is dim and dark. A shaft of light enters the hut from a small hole in the thatched roof. A trapdoor in the floor leads down.')
            self.location.passage_revealed = True
            return True
        return False

    def take(self, p, cons, oDO, oIDO):
        self.reveal_trapdoor(p, cons, oDO, oIDO)
        return super().take(p, cons, oDO, oIDO)
    
    def move(self, p, cons, oDO, oIDO):
        if not self.reveal_trapdoor(p, cons, oDO, oIDO):
            cons.user.perceive("You move the rug, and nothing happens.")
            self.location.emit("&nD%s moves the rug, and nothing happens." % cons.user.name(), ignore=[cons.user])
        return True

    
    actions = dict(thing.Thing.actions)
    actions['take'] = action.Action(take, True, False)
    actions['get'] = action.Action(take, True, False)
    actions['move'] = action.Action(move, True, False)


def clone():
    return Rug()
