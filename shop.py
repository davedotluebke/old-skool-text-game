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
        self.change_currencies = [gametools.clone('currencies.gold'), gametools.clone('currencies.silver'), gametools.clone('currencies.copper')]
        Thing.game.schedule_event(120, self.restock, None)
        self.obj_classes_accepted = []
        self.obj_class_error_msg = "Sorry, I don't deal in those."
    
    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #

    def _decide_if_will_buy(self, item):
        """Decide if the shopkeeper will buy the item. Can be overloaded for more complex functionality."""
        if self.obj_classes_accepted: # If this is empty or None, accept everything
            for i in self.obj_classes_accepted:
                if isinstance(item, i):
                    return True
            return False
        return True

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
        if not self.location:
            return
        for i in self.location.contents:
            if hasattr(i, 'cons') and i not in self.welcomed_customers:
                self.say(self.welcome_message)
                self.welcomed_customers.append(i)
        for j in self.welcomed_customers:
            if j not in self.location.contents:
                del self.welcomed_customers[self.welcomed_customers.index(j)]

    def restock(self, unnecesary_parameter):
        for i in self.default_items:
            self.inventory.append(gametools.clone(i.path))
        Thing.game.events.schedule(Thing.game.time+120, self.restock, None)

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
            # possible_inventory_matches is the direct object (if we don't pass it in, this code will break)
            return possible_inventory_matches[0].look_at(p, cons, possible_inventory_matches[0], oIDO)
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
        for item in self.inventory:
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

        player_money = sorted(player_money, key=Money.get_unit_value)

        # Select the exact money the player is going to spend
        using_to_pay = []
        payment_total = 0
        for coin in player_money:
            if payment_total >= item.get_total_value():
                break
            if coin.get_total_value() + payment_total >= item.get_total_value() and coin.plurality > 1:
                for i in range(1, coin.plurality+1):
                    payment_total += coin.get_unit_value()
                    if payment_total >= item.get_total_value():
                        new_coin = coin.replicate()
                        new_coin.plurality = i
                        coin.plurality -= i
                        using_to_pay.append(new_coin)
                        break
            else:  # Need all of this type of coin
                payment_total += coin.get_total_value()
                using_to_pay.append(coin)

        saying_to_customer = "I am taking"
        for coin in using_to_pay:
            saying_to_customer += " %s %s" % (coin.plurality, coin.names[0])
            coin.move_to(self, force_move=True)
        self.say(saying_to_customer)

        coins = get_change(payment_total - item.get_total_value(), self.change_currencies)
        saying_to_customer = "I am giving you"
        for coin in coins:
            saying_to_customer += " %s %s" % (coin.plurality, coin.names[0])
            coin.move_to(cons.user)
        if saying_to_customer != "I am giving you":
            self.say(saying_to_customer)
        
        item.move_to(cons.user)
        cons.user.perceive("You purchase the %s." % item)
        return True
    
    def sell(self, p, cons, oDO, oIDO):
        """Sell an item to the shop."""
        # First, find the item the user wants to sell
        item = oDO
        if not item:
            return "Not sure what you are trying to sell!"
        """ (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)

        matches = p.find_matching_objects(sDO, cons.user.contents, cons)
        if matches == False:
            return True # find_matching_object found multiple ambiguous objects and printed error message
        elif not matches:
            return 'You aren\'t carrying a %s!' % sDO
        elif len(matches) > 1:
            return 'Please sell one type of item at a time.'
        item = matches[0] # Found the item they are trying to sell """

        # Next, check if the shop accepts this kind of item
        if not self._decide_if_will_buy(item):
            self.say(self.obj_class_error_msg)
            return True
        # Next, give the player their money
        coins = get_change(item.get_total_value(), self.change_currencies)
        going_to_say = "Thank you for the %s! I am giving you" % item
        for i in coins:
            going_to_say += " %s %s" % (i.plurality, i.names[0])
            i.move_to(cons.user)
        self.say(going_to_say)
        # Lastly, take the item
        item.move_to(self, True)
        self.inventory.append(item)
        return True

    actions = dict(NPC.actions)
    actions['look'] =     Action(look_at, True, True)
    actions['examine'] =  Action(look_at, True, False)
    actions['inspect'] =  Action(look_at, True, False)
    actions['buy'] =      Action(buy, True, False)
    actions['sell'] =     Action(sell, True, False)
    actions['purchase'] = Action(buy, True, False)
