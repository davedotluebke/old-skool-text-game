from debug import dbg
from thing import Thing
from action import Action

class Container(Thing):
    def __init__(self, ID):
        Thing.__init__(self, ID)
        self.contents = []
        self.max_weight_carried = 1
        self.max_volume_carried = 1

    def insert(self, obj):
        """Put obj into this Container object, returning True if the operation failed"""
        dbg.debug("in insert")
        # error checking for max weight etc goes here
        if obj.id == self.id:
            dbg.debug('Trying to insert into self - not allowed!')
            return True
        contents_weight = 0
        contents_volume = 0
        dbg.debug("going to start looping")
        for w in self.contents:
            contents_weight = contents_weight + w.weight
            contents_volume = contents_volume + w.volume
        dbg.debug("done looping - carrying %d weight and %d volume" % (contents_weight, contents_volume))
        if self.max_weight_carried >= contents_weight+obj.weight and self.max_volume_carried >= contents_volume+obj.volume:
            dbg.debug("%s has room for %s's %d weight and %d volume" % (self.id, obj.id, obj.weight, obj.volume))
            obj.set_location(self)   # make this container the location of obj
            self.contents.append(obj)
            return False
        else:
            dbg.debug("The weight(%d) and volume(%d) of the %s can't be held by the %s, "
                  "which can only carry %d grams and %d liters (currently "
                  "holding %d grams and %d liters)" 
                  % (obj.weight, obj.volume, obj.id, self.id, self.max_weight_carried, self.max_volume_carried, contents_weight, contents_volume))
            return True

    def set_max_weight_carried(self, max_grams_carried):
        self.max_weight_carried = max_grams_carried

    def set_max_volume_carried(self, max_liters_carried):
        self.max_volume_carried = max_liters_carried

    def extract(self, obj):
        """Remove obj from this Container, returning True if the operation failed"""
        if obj not in self.contents:
            dbg.debug("Error! ",self.id," doesn't contain item ",obj.id)
            return True
        
        found = -1
        for i in range(0, len(self.contents)):
            if obj == self.contents[i]:
                found = i
                break
        assert found != -1
        del self.contents[i]

    def look_at(self, p, cons, oDO, oIDO):
        dbg.debug("Called Container.look_at()")
        result = Thing.look_at(self, p, cons, oDO, oIDO)
        if result != True:
            return result
        if bool(len(self.contents)):   # TODO: lose bool and len functions?
            cons.write("Inside there is:")
            for item in self.contents:
                cons.write(item.short_desc)
        else:
            cons.write("It is empty.")
        return True

