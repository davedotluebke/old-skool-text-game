import home.scott.house.faucetThings as faucetThings
import action


class WaterFountain(faucetThings.FaucetThing):
    def drink(self, p, cons, oDO, oIDO):
        if oIDO == self:
            cons.user.perceive('You graciously drink the cool water and it quenches your thirst.')
            self.emit('&nD%s graciously drinks from the water fountain.' % cons.user.id)
            return True
        else:
            return 'I don\'t see what you are trying to drink!'
    
    def toggle(self, p, cons, oDO, oIDO):
        value = super().toggle(p, cons, oDO, oIDO)
        if value != True:
            return value
        else:
            cons.game.schedule_event(2, self.turn_off)
    
    def turn_off(self):
        self.running = 0
        self._adjust_descriptions()
        self.emit('The water fountain turns off.')
    
    actions = dict(faucetThings.FaucetThing.actions)
    actions['drink'] = action.Action(drink, True, True)
    actions['turn']  = action.Action(toggle, True, False)
    actions['activate'] = action.Action(toggle, True, False)

def clone():
    water_fountian = WaterFountain('fountain', __file__, 'simple water fountian', 'This is a simple copper water fountain, there is nothing abnormal about it.', 'fountain')
    water_fountian.add_adjectives('water', 'simple', 'metal', 'drinking')
    water_fountian.add_names('faucet')
    return water_fountian