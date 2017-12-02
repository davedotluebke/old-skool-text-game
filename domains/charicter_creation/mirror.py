import thing

class Mirror(thing.Thing):
    def __init__(self, what_you_see, exit_room):
        super().__init__('mirror', __file__)
        self.set_description('shimmering mirror', 'In this mirror you see %s.' % what_you_see)
        self.actions.append(thing.Action(self.enter, ['enter'],True, False))
        self.dest = exit_room
        self.add_race = None
        self.add_gender = None

    def enter(self, p, cons, oDO, oIDO):
        if self.add_race:
            cons.user.race = self.add_race
        if self.add_gender:
            cons.user.gender = self.add_gender
        cons.user.move_to(self.dest)
        self.dest.report_arrival(cons.user)
