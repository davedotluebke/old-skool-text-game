import gametools
import scenery
import room
import action

class LargeTree(scenery.Scenery):
    def __init__(self):
        super().__init__("tree", "large tree", "This large pine tree towers above the others. At the top you can barely make out what appears to be a bird's nest.", unlisted=True)
        self.add_adjectives("large", "pine", "tall")
        self.add_names("pine")
        self.rope_attached = False
        self.actions['climb'] = action.Action(LargeTree.climb, True, False)
        self.actions['ascend'] = action.Action(LargeTree.climb, True, False)
        self.actions['throw'] = action.Action(LargeTree.throw, True, False)
    
    def throw(self, p, cons, oDO, oIDO):
        """Throw the rope at the tree."""
        if oIDO != self:
            return "Did you mean to throw the %s at the tree?" % oDO.name()

        if self.rope_attached:
            cons.user.perceive("There's already a rope attached to the tree!")
            return True

        if oDO.name() != "rope":
            cons.user.perceive("The %s doesn't seem like the right tool for the job." % oDO.name())
            return True

        cons.user.perceive("You throw the rope at the tree, catching it on one of the high branches.")
        oDO.move_to(self.location)
        oDO.fix_in_place("The rope is tied to the tree.")
        self.rope_attached = True
        self.location.add_exit('up', 'domains.centrata.mountain.treetop')
        return True
    
    def climb(self, p, cons, oDO, oIDO):
        """Attempt to climb the tree."""
        if oDO != self:
            return "Did you mean to climb the large pine tree?"

        if not self.rope_attached:
            if not oIDO:
                cons.user.perceive("You can't reach the higher sturdy branches with your bare hands.")
                return True

            if oIDO.name() != "rope":
                cons.user.perceive("You can't use the %s to climb the tree." % oIDO.name())
                return True

            self.throw(p, cons, oIDO, oDO) # intentionally swapped due to the syntax differences

        cons.user.perceive("You climb up the tree to a higher spot.")
        self.emit("&nD%s climbs the tree." % cons.user, ignore=[cons.user])
        cons.user.move_to(gametools.load_room('domains.centrata.mountain.treetop'))
        return True
    
    

def load():
    roomPath =  gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists
    
    trail = room.Room('trail', roomPath)
    trail.set_description('winding trail through the woods', 'The trail continues through a tall wood of pines. Many of the trees stretch far above the ground. One particularly large tree catches your eye.')
    trail.add_exit('east', 'domains.centrata.mountain.base')
    trail.add_exit('west', 'domains.centrata.mountain.mountain_laurel')

    small_tree = scenery.Scenery("tree", "small tree", "This small pine tree is growing in the shadow of the larger tree.", unlisted=True)
    small_tree.add_adjectives("small", "pine", "short")
    small_tree.add_names("pine")
    small_tree.add_response(['climb', 'ascend'], 'The tree bends over and you fall off. It then springs back up.')
    trail.insert(small_tree, True)

    large_tree = LargeTree()
    trail.insert(large_tree, True)
    
    return trail
