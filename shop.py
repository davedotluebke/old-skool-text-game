from thing import Thing
from room import Room
from creature import NPC
from debug import dbg
from action import Action
from money import Money
from money import get_change
import gametools

class Shopkeeper(NPC):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, inventory_file):
        super().__init__(default_name, path)
        # TODO: Loading saved shop inventory goes here
        self.inventory = [] # XXX replace
        self.default_items = []
        self.welcome_message = 'Welcome to my shop!'
        self.welcomed_customers = []
        Thing.game.events.schedule(120, self.restock, None)
    
    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    #
    # SET/GET METHODS (methods to set or query attributes)
    #
    def add_items(self, *sItems):
        """Add items to the shop, each as a seperate argument."""
        self.inventory += [x for x in list(sItems) if isinstance(x, Thing)] #TODO: Handle pluralities inside the shop's inventory

    def get_items(self):
        """Get a list of items that are currently in the shop."""
        return self.inventory
    
    def remove_items(self, *sItems):
        """Remove the specified items from the shop, returning the sucessfully removed ones as a list."""
        items = []
        for x in list(sItems):
            try:
                i = self.inventory.index(x) #TODO: Handle pluralities inside the shop's inventory
            except ValueError:
                dbg.debug("Error! Shop %s doesn't contain item %s!" % (self, x))
                continue
            items.append(self.inventory[i])
            del self.inventory[i]
        return items
    
    def set_default_items(self, *sItems):
        """Set the default items in the shop, each specified by a seperate argument."""
        self.default_items = [x for x in list(sItems) if isinstance(x, Thing)]
    
    def set_welcome_message(self, msg):
        self.welcome_message = msg

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def heartbeat(self):
        # TODO: Respond to being attacked 
        
        # Greet any new players who enter the room
        for i in self.location.contents:
            if i not in self.welcomed_customers:
                self.say(self.welcome_message)
                self.welcomed_customers.append(i)
        for j in self.welcomed_customers:
            if j not in self.location.contents:
                del self.welcomed_customers[self.welcomed_customers.index(j)]

    def restock(self, unnecesary_parameter):
        for i in self.default_items:
            self.inventory.append(gametools.clone(i.path))
        Thing.game.events.schedule(120, self.restock, None)

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    # 
    def look_at(self, p, cons, oDO, oIDO):
        """Look at the shopkeeper, or alternitavely, an item in the shop."""
        if oDO == self or oIDO == self:
            return super().look_at(p, cons, oDO, oIDO)
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if sDO in ['shop', 'inventory'] or sIDO in ['shop', 'inventory']:
            return self.list_inventory(p, cons, oDO, oIDO)
        possible_inventory_matches = []
        for i in self.inventory:
            if sDO in i.names or sIDO in i.names:
                possible_inventory_matches.append(i)
        if len(possible_inventory_matches) == 0:
            return "Did you mean to look at something in the shop?"
        elif len(possible_inventory_matches) == 1:
            return possible_inventory_matches[0].look_at(p, cons, oDO, oIDO):
        elif len(possible_inventory_matches) > 1:
            new_str = "Did you mean to look at"
            for j in possible_inventory_matches:
                new_str += " "
                new_str += j.get_short_desc()
                if len(possible_inventory_matches) - possible_inventory_matches.index(j) > 1:
                    new_str += ","
                elif len(possible_inventory_matches) - possible_inventory_matches.index(j) == 1:
                    new_str += ", or"
            new_str += "?"
            return new_str

    def list_inventory(self, p, cons, oDO, oIDO):
        """List the inventory of this shop."""
        cons.user.perceive('The shop is selling: ')
        for item in self.contents:
            cons.user.perceive(item.get_short_desc(indefinite=True))
        return True
    
    def buy(self, p, cons, oDO, oIDO):
        """Buy an item from the shop."""
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)

        # First, see if the object is in the shop's inventory
        matches = p.find_matching_objects(sDO, self.inventory, cons)
        if matches == False:
            return True # find_matching_object found multiple ambiguous objects and printed error message
        elif not matches:
            return 'The shop does not seem to sell "%s".' % sDO
        elif len(matches) > 1:
            return 'Please purchase one type of item at a time.'
        item = matches[0] # Found the item they are trying to buy
        
        # Second, verify that the player has enough money
        player_money = []
        player_money_value = 0
        for o in cons.user.contents:
            if isinstance(o, Money):
                player_money.append(o)
                player_money_value += o.get_total_value()
        if player_money_value < item.get_total_value():
            cons.user.perceive("You don't have enough money to buy the %s!" % item)
            return True

        player_money = sorted(player_money, key=Money.get_unit_value, reverse=True)

        #XXX code beyond this point does not work
        using_to_pay = []
        player_money_value = 0
        for coin in player_money:
            player_money_value += coin.get_total_value()
            using_to_pay.append(coin)
            if player_money_value > item.get_total_value():
                break
        
        for coin in using_to_pay:
            coin.move_to(self, force_move=True)
        coins = get_change(player_money_value, [gametools.clone('gold'), gametools.clone('silver'), gametools.clone('copper')])
        for coin in coins:
            coin.move_to(cons.user)

    actions = dict(NPC.actions)
    actions['look'] = Action(look_at, True, True)
    actions['examine'] = Action(look_at, True, False)
    actions['inspect'] = Action(look_at, True, False)
