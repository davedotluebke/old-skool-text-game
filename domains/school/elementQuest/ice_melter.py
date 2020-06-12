import container
import gametools
import scenery
import thing

class melting(container.Container):
    def insert(self, obj, force_insert=False, merge_pluralities=True):
        if super().insert(obj, force_insert, merge_pluralities):
            return True
        if 'ice' in obj.names:
            self.emit ('The ice slowly melts, filling the room with a hot steam.')
            self.location.set_description('steamy sauna', 'You walk into a sauna, it is very steamy making it hard to see.')
            obj.set_description('melting ice block', 'This ice is melting fast, giving off a thick cloud of steam.')
            thing.Thing.game.schedule_event(15, self.end_steam, obj)
    def end_steam(self, obj):
        self.emit('The steam clears making it easier to see.')
        obj.destroy()
        self.location.set_description( 'sauna', 'You go through a glass door and enter a suana.')

def clone():
    ice_melter = melting('melter', __file__)
    ice_melter.fix_in_place('You try as hard as you can but you just can\'t budge the ice melter.')
    ice_melter.add_adjectives('hot', 'ice', 'small', 'normal')
    ice_melter.set_description('ice melter', 'This is a small but normal ice melter. It is hot.')
    ice_melter.set_max_volume_carried(2.5)
    ice_melter.set_max_weight_carried(2000)
    return ice_melter