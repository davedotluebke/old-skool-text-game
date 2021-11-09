import creature
import domains.centrata.orc_quest.prairie as prairie

class Orc(creature.NPC):
    def attack(self, enemy):
        if not isinstance(enemy, Orc):
            return super().attack(enemy)
        else:
            self.log.warning('Orcs are disabled from attacking other orcs.')
            if self.attacking == enemy:
                self.attacking = False
            if enemy in self.enemies:
                self.enemies.remove(enemy)

    def set_orc_range(self, orc_range):
        """Set the orc range, which defines how far (in rooms) the orc 
        will wander from the orc camp."""
        self.orc_range = orc_range

    def is_forbidden(self, r):
        """Check whether the creature is allowed to enter room `r`.
        `r` is string containing the path to the room
        return True if the room is forbidden."""
        try:
            xy_list = r.partition('?')[2].split('&')
            x = int(xy_list[0])
            y = int(xy_list[1])

            if abs(x - prairie.orc_camp_x) > self.orc_range or abs(y - prairie.orc_camp_y) > self.orc_range:
                return True
            else:
                return False
        except:
            self.log.exception("Room name does not follow prairie template!")
            return True
