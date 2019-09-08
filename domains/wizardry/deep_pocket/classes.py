import sys
import gametools
from action import Action
from thing import Thing
from container import Container
from creature import NPC
from player import Player
from room import Room

class DeepPocket(Container):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, exit_loc, user, path, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_max_volume_carried(sys.maxsize)
        self.set_max_weight_carried(sys.maxsize)
        self.exit_loc = exit_loc
        self.user = user
    
    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def exit_vault(self, p, cons, oDO, oIDO):
        cons.write("You exit the vault.")
        cons.user.move_to(self.exit_loc)
        self.exit_loc.report_arrival(cons.user)

    actions = dict(Container.actions)
    actions['exit'] = Action(exit_vault, True, True)

class DeepPocketSignUpWizard(NPC):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, path):
        super().__init__("Silemon", path, pref_id="DeepPocketSignUpWizard")
        self.set_description("Silemon Deplintere", "Silemon Deplintere is an older wizard and is wearing a blue cape. He is standing uniformly in front of you.")
        self.deep_pockets = []
        for i in Thing.ID_dict:
            if isinstance(i, DeepPocket):
                self.deep_pockets.append(i)
        self.serving_customer = False
        self.vault_room = gametools.load_room('domains.wizardry.deep_pocket.vaults')
        self.in_process = False
        self.said_nos = []

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        if not self.location:
            return
        customers = []
        for p in self.location.contents:
            if isinstance(p, Player):
                prev = False
                if p in self.said_nos:
                    prev = True
                for d in self.deep_pockets:
                    if d.user == p:
                        prev = True
                for i in p.contents:
                    if isinstance(i, DeepPocket):
                        prev = True
                if not prev and p != self.serving_customer:
                    customers.append(p)
        if not customers and not self.serving_customer:
            return
        if not self.serving_customer:
            self.emit('Silemon says: "Next up is %s!"' % customers[0])
            self.serving_customer = customers[0]
            self.serving_customer.perceive('Silemon says to you: "I\'m just double-checking - you\'re here for a deep pocket, right?"')
        if not self.serving_customer.cons:
            self.serving_customer = None

    def create_new_pocket(self, customer):
        DeepPocket.vault_room = self.vault_room
        DeepPocket.customer = customer
        new_pocket = gametools.clone('domains.wizardry.deep_pocket.pocket')
        DeepPocket.customer = None
        new_pocket.move_to(customer)
        customer.cons.write('Silemon says: Ok, this will just take a second...')
        Thing.game.events.schedule(Thing.game.time+3, self.finish_pocket, customer)
        self.in_process = True
        self.deep_pockets.append(new_pocket)

    def finish_pocket(self, customer):
        customer.cons.write('Silemon takes a jade out of his pocket, makes some strange motions, and puts it back.')
        customer.cons.write('Silemon says: "Your deep pocket is ready! Enjoy!"')
        self.serving_customer = False
        self.in_process = False

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def reply(self, p, cons, oDO, oIDO):
        if cons.user != self.serving_customer:
            return "It's not your turn yet!"
        reply = p.words[0]
        if not reply:
            return "Were you trying to reply to Silemon?"
        if reply.lower() == 'yes':
            self.create_new_pocket(self.serving_customer)
        elif reply.lower() == 'no':
            self.serving_customer.cons.write('Silemon says: "Ok, if that\'s what you want."')
            self.serving_customer = False
        return True

    actions = dict(NPC.actions)
    actions['yes'] = Actions(reply, False, True)
    actions['no'] =  Actions(reply, False, True)
    
class VaultRoom(Room):
    def heartbeat(self):
        for i in self.contents:
            if isinstance(i, Player):
                for l in self.vaults:
                    if l.user == i:
                        i.move_to(l)

