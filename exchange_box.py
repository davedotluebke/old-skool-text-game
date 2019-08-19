from container import Container
from money import get_change
import gametools

class ExchangeBox(Container):
    def insert(self, obj, force_insert, merge_pluralities):
        if not super().insert(obj, force_insert, merge_pluralities):
            amt = 0
            for i in self.contents:
                amt += i.get_value()
                i.destroy()
            change = get_change(amt, [gametools.clone('gold'), gametools.clone('silver'), gametools.clone('copper')])
            for j in change:
                super().insert(j)
            return False
        return True

def clone():
    e = ExchangeBox('box', __file__)
    e.set_description('exchange box', 'This is a test exchange box.')
    return e
