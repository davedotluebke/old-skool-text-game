import creature
import gametools
import random

class Cartographer(creature.NPC):
    def __init__(self):
        super().__init__("cartographer", __file__)
        self.set_description("weathered cartographer", "This cartographer looks as if he has travelled the entire world.")
        self.add_adjectives("weathered")
        self.proper_name = "Cartus" # probably irrelevant since we currently don't have NPCs automatically introduce themselves
        self.gender = "male" # same as above

        self.prev_location = ""
        self.visited_rooms = []
        self.map = {}
        self.south_index = 0
        self.east_index = 0
        self.up_index = 0
        self.lowest_index = 0
        self.highest_index = 0

    def get_index_str(self):
        return str([self.south_index, self.east_index, self.up_index])

    def heartbeat(self):
        if self.dead:
            # if killed, return to the starting room and keep going
            self.move_to(gametools.load_room("home.johanna.house.lr31795"))
            self.heath = self.hitpoints
        if self.health < self.hitpoints:
            self.heal()
        
        # this is the code that actually does the mapping
        # first, if the current location is not in the map, add it
        if self.get_index_str() not in self.map.keys():
            self.map[self.get_index_str()] = self.location.id
        
        # next, find the next unexplored room to go to
        """next_exit_dir = ""
        for i in self.location.exits.keys():
            if self.location.exits[i] not in self.map[str([self.south_index, self.east_index, self.up_index])]:
                next_exit_dir = i"""
        
        # if no new room found, go to anywhere except the previous location
        possible_exits = [x for x in self.location.exits.keys() if x not in self.visited_rooms]
        if not possible_exits:
            return

        next_exit_dir = random.choice(possible_exits)
        
        # set the previous location to make sure the cartographer doesn't wander in circles
        self.prev_location = self.location.id
        self.visited_rooms.append(self.location.id)

        # update the indecies
        self.update_indicies(next_exit_dir)
        
        self.go_to_room(self.location.exits[next_exit_dir], next_exit_dir, ignore_monster_safe=True)
    
    def perceive(self, message):
        super().perceive(message)

        if "map" in message.split(" "):
            self.say("Here is my map:")
            # then print the map
            self.print_map()
    
    def update_indicies(self, dir):
        if dir == "north":
            self.south_index -= 1
        
        elif dir == "south":
            self.south_index += 1
        
        elif dir == "west":
            self.east_index -= 1
        
        elif dir == "east":
            self.east_index += 1
        
        elif dir == "northwest":
            self.south_index -= 1
            self.east_index -= 1
        
        elif dir == "northeast":
            self.south_index -= 1
            self.east_index += 1
        
        elif dir == "southwest":
            self.south_index += 1
            self.east_index -= 1
        
        elif dir == "southeast":
            self.south_index += 1
            self.east_index += 1
        
        elif dir == "up":
            self.up_index += 1
        
        elif dir == "down":
            self.up_index -= 1

        if self.south_index < self.lowest_index:
            self.lowest_index = self.south_index
        
        if self.east_index < self.lowest_index:
            self.lowest_index = self.east_index
        
        if self.up_index < self.lowest_index:
            self.lowest_index = self.up_index

        if self.south_index > self.highest_index:
            self.highest_index = self.south_index
        
        if self.east_index > self.highest_index:
            self.highest_index = self.east_index
        
        if self.up_index > self.highest_index:
            self.highest_index = self.up_index

    def print_map(self):
        for i in range(self.lowest_index, self.highest_index+1):
            for j in range(self.lowest_index, self.highest_index+1):
                for k in range(self.lowest_index, self.highest_index+1):
                    try:
                        print(self.map[str([j, k, i])].ljust(10)[-10:-1], end="")
                    except KeyError:
                        print(" " * 10, end="")
                print("\n", end="")
            print("\n\n", end="")

def clone():
    return Cartographer()
