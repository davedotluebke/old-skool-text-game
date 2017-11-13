import thing
import gametools

class Fireplace(thing.Thing):
    def __init__(self):
        super().__init__('fireplace', __file__)
        self.set_description('enourmous fireplace', 'This enourmous fireplace is filled with logs that are slowly burning. '
        'It almost seems as if there were another room also facing this fireplace, but you can\'t be sure.', unlisted=True)
        self.add_adjectives('enourmous', 'huge')
        self.actions.append(thing.Action(self.enter, ['enter'], True, False))
        self.dest = 'domains.school.school.fire_lounge'

    def enter(self, p, cons, oDO, oIDO):
        if oDO != self:
            return "What do you intend to enter?"
        if cons.user.wizardry_element == 'fire':
            if self.dest == 'domains.school.school.fire_lounge':
                cons.user.perceive("You stealthily pass through the fireplace, and find yourself in another room.")
            else:
                cons.user.perceive("You pass through the fireplace into the Great Hall.")
                self.emit('&d%s passes through the fireplace to a room on the other side. ' % cons.user, ignore = [cons.user])
            dest = gametools.load_room(self.dest)
            if not dest:
                return "Whoops! There isn't actually a room on the other side!"
            cons.user.move_to(dest)
            dest.report_arrival(cons.user)
            return True
        else:
            cons.user.perceive('You burn yourself in the flames of the fire, and it pushes you away.')
            cons.user.health -= 2
            return True

def clone():
    return Fireplace()
