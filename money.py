from thing import Thing

class Money(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, value, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_value(value)

#
# MODULE-LEVEL FUNCTIONS (e.g., clone() or load())
#
def get_change(amt, currencies):
    """Given an amount and a list of currency objects, return change in the smallest number of coins possible.
    The currencies list is a list of objects of the Money class in decending order of value (e.g. gold, silver,
    copper)."""
    coin_objects = []
    for currency in currencies:
        if not currency:
            continue
        number_of_coins = amt // currency.get_total_value()
        amt -= number_of_coins * currency.get_total_value()
        if number_of_coins > 0:
            new_coin = currency.replicate()
            new_coin.plurality = number_of_coins
            coin_objects.append(new_coin)
    return coin_objects
