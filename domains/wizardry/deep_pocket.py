import sys
from action import Action
from thing import Thing
from container import Container
from creature import NPC
from player import Player

class DeepPocket(Container):
    def __init__(self, default_name, exit_loc, user, pref_id=None):
        super().__init__(default_name, pref_id)
        self.set_max_volume_carried(sys.maxsize)
        self.set_max_weight_carried(sys.maxsize)
        self.exit_loc = exit_loc
        self.actions.append(Action(self.exit_vault, ['exit'], True, False))
        self.user = user
    
    def exit_vault(self, p, cons, oDO, oIDO):
        cons.write("You exit the vault.")
        cons.user.move_to(self.exit_loc)
        self.exit_loc.report_arrival(cons.user)

class DeepPocketSignUpWizard(NPC):
    def __init__(self, vault):
        super().__init__("Silemon", Thing.ID_dict['nulspace'].game, pref_id="DeepPocketSignUpWizard")
        self.set_description("Silemon Deplintere", "Silemon Deplintare is an older wizard and is wearing a blue cape. He is standing uniformly in front of you.")
        self.deep_pockets = []
        for i in Thing.ID_dict:
            if isinstance(i, DeepPocket):
                self.deep_pockets.append(i)
        self.serving_customer = False
        self.vault_room = vault
        self.in_process = False

    def heartbeat(self):
        customers = []
        for p in self.location.contents:
            if isinstance(p, Player):
                prev = False
                for d in self.deep_pockets:
                    if d.user == p:
                        prev = True
                if not prev and p != self.serving_customer:
                    customers.append(p)
        if not customers and not self.serving_customer:
            return
        if not self.serving_customer:
            self.emit('Silemon says: "Next up is %s!"' % customers[0])
            self.serving_customer = customers[0]
        if self.in_process == True:
            return
        self.serving_customer.cons.write('Silemon says to you: "I\'m just double-checking - you\'re here for a deep pocket, right?"')
        while True: #XXX replace with system that will work with multiplayer
            self.serving_customer.cons.write('Type "yes" to answer yes to the question, and "no" to answer no to it.')
            reply = self.serving_customer.cons.take_input(':')
            if reply.lower() == 'yes':
                self.create_new_pocket(self.serving_customer)
                break
            elif reply.lower() == 'no':
                self.serving_customer.cons.write('Silemon says: "Ok, if that\'s what you want."')
                self.serving_customer = False
                break
            else:
                self.serving_customer.cons.write('Did you mean "yes" or "no"?')

    def create_new_pocket(self, customer):
        new_pocket = DeepPocket('pocket', self.vault_room, customer)
        new_pocket.set_description('deep pocket', 'This is a magical deep pocket. Putting things in the pocket transports them to an infinite space vault.')
        new_pocket.move_to(customer)
        customer.cons.write('Just a moment, please...')
        Thing.ID_dict['nulspace'].game.events.schedule(Thing.ID_dict['nulspace'].game.time+2, self.finish_pocket, customer)
        self.in_process = True
        self.deep_pockets.append(new_pocket)
    def finish_pocket(self, customer):
        customer.cons.write('Silemon takes a jade out of his pocket, makes some strange motions, and puts it back.')
        customer.cons.write('Silemon says: "Your deep pocket is ready! Enjoy!"')
        self.serving_customer = False
        self.in_process = False
        