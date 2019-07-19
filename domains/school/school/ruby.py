import domains.wizardry.gems as gems
import domains.school.school.profsun as profsun

class ProfSunRuby(gems.Ruby):
    def __init__(self):
        super().__init__(__file__, 'ruby', 'large red ruby', 'This large red ruby feels like it carries a sense.')
        gems.Thing.game.register_heartbeat(self)

    def heartbeat(self):
        super().heartbeat()
        if self.power_num > 0:
            if self not in profsun.ProfSun.rubies_powered:
                profsun.ProfSun.rubies_powered.append(self.location)

def clone():
    return ProfSunRuby()
