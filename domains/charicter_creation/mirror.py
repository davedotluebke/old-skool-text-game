import thing

class Mirror(thing.Thing):
    def __init__(self, what_you_see, exit_room):
        super().__init__('mirror', __file__)
        self.set_description('shimmering mirror', 'In this mirror you see %s.' % what_you_see)
        self.actions.append(thing.Action(self.enter, ['enter'],True, False))
        self.dest = exit_room

    def enter(self, p, cons, oDO, oIDO):
        cons.user.move_to(self.dest)
        self.dest.report_arrival(cons.user)
