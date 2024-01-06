import thing
import player
import action

directions = {'north': (0, -1,  0 ), 
            'south': (0,  1,  0 ),
            'east':  (1,  0,  0 ),
            'west':  (-1, 0,  0 ),
            'northwest': (-1, -1, 0),
            'southeast': (1, 1, 0),
            'northeast': (1, -1, 0),
            'southwest': (-1, 1, 0),
            'up':    (0,  0,  1 ), 
            'down':  (0,  0, -1 )}

opposite_directions = {
        'north':     'south',
        'south':     'north',
        'east':      'west',
        'west':      'east',
        'down':      'up',
        'up':        'down',
        'northwest': 'southeast',
        'northeast': 'southwest',
        'southeast': 'northwest',
        'southwest': 'northeast'
}

class Map(thing.Thing):
    def __init__(self):
        super().__init__("map", __file__)
        self.set_description("old map", "This is an old and worn-looking map. (Hint: Try \"Read Map\" to get more information.)")
        self.add_adjectives("old", "worn")
        
        self.game.register_heartbeat(self)

        self.coordinates = (0, 0, 0)
        self.map = {}
        self.map_room_chars = {}
        self.visited_rooms = {}
        self.prev_player_location = None

    def heartbeat(self):
        if type(self.location) != player.Player:
            return
        
        # find if the player has moved and update the coordinates
        if self.location.location != self.prev_player_location: # if the player has moved
            if self.prev_player_location: # when starting out, just initialise the current location
                if self.location.location.id not in self.visited_rooms:
                    for i in self.prev_player_location.exits:
                        if self.prev_player_location.exits[i] == self.location.location.id:
                            self.coordinates = (self.coordinates[0] + directions[i][0], self.coordinates[1] + directions[i][1], self.coordinates[2] + directions[i][2]) # update the coordinates to the new room
                            self.visited_rooms[self.location.location.id] = self.coordinates
                else:
                    self.coordinates = self.visited_rooms[self.location.location.id]
            
            # TODO: something here if the player teleported, etc and there's no direct connection

            self.prev_player_location = self.location.location

        # update the exits at the current coordinates
        self.map[self.coordinates] = list(self.location.location.exits)
        # update the name of the current room (based on the first letter last item in the room's id)
        self.map_room_chars[self.coordinates] = self.location.location.id.rpartition(".")[2][0]
    
    def read(self, p, cons, oDO, oIDO):
        cons.write(self.print_map())
        return True
    
    def print_map(self):
        coordinate_pairs = list(self.map.keys())
        # find the lowest and highest numbered x, y, z
        lowest_x = 0
        lowest_y = 0
        lowest_z = 0
        highest_x = 0
        highest_y = 0
        highest_z = 0
        for i in coordinate_pairs:
            if i[0] < lowest_x:
                lowest_x = i[0]
            if i[1] < lowest_y:
                lowest_y = i[1]
            if i[2] < lowest_z:
                lowest_z = i[2]
            
            if i[0] > highest_x:
                highest_x = i[0]
            if i[1] > highest_y:
                highest_y = i[1]
            if i[2] > highest_z:
                highest_z = i[2]
        
        # make the map
        final_map = ""
        for z in range(lowest_z, highest_z+1):
            level = "Level " + str(z) + ":\n"
            for y in range(lowest_y, highest_y+1):
                line1 = ""
                line2 = ""
                line3 = ""
                for x in range(lowest_x, highest_x+1):
                    if (x, y, z) not in list(self.map.keys()):
                        line1 += "   "
                        line2 += "   "
                        line3 += "   "
                        continue
                    line1 += "\\" if "northwest" in self.map[(x, y, z)] else " "
                    line1 += "|" if "north" in self.map[(x, y, z)] else " "
                    line1 += "/" if "northeast" in self.map[(x, y, z)] else " "
                    line2 += "-" if "west" in self.map[(x, y, z)] else " "
                    line2 += self.map_room_chars[(x, y, z)]
                    line2 += "-" if "east" in self.map[(x, y, z)] else " "
                    line3 += "/" if "southwest" in self.map[(x, y, z)] else " "
                    line3 += "|" if "south" in self.map[(x, y, z)] else " "
                    line3 += "\\" if "southeast" in self.map[(x, y, z)] else " "
                level += line1 + "\n" + line2 + "\n" + line3 + "\n"
            level += "\n\n"
            final_map += level
        print(final_map)
        return '```\n' + final_map + '\n```'
    
    def save_ouput(self, filename):
        f = open(filename, 'w')
        f.write(self.print_map())
        f.close()

    def inscribe(self, p, cons, oDO, oIDO):
        self.save_ouput('map.txt')
        cons.user.perceive('You inscribe the map, etching it into permanance.')
        return True

    actions = dict(thing.Thing.actions)
    actions['read'] = action.Action(read, True, True)
    actions['inscribe'] = action.Action(inscribe, True, False)

def clone():
    return Map()
