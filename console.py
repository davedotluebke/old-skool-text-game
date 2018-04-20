import asyncio
import connections_websock
from textwrap import TextWrapper

from debug import dbg
from parse import Parser
from player import Player

class Console:
    default_width = 80
    prompt = "--> "
    help_msg = """Your goal is to explore the world around you, solve puzzles,
               fight monsters, complete quests, and eventually become a
               Sorcerer capable of changing and adding to the very fabric 
               of the world itself.\n\n
               Useful commands include 'look' to examine your surroundings 
               or an object, 'take' to pick something up, 'inventory' to see 
               what you are carrying, 'go' to move a particular direction. 
               You can use prepositions to create more complex commands and
               adjectives to specify particular objects; articles are 
               optional. Here are some examples of valid commands:\n\n
               \t'look'\n
               \t'go north'\n
               \t'take sword'\n
               \t'take the rusty sword'\n
               \t'drink potion from tall flask'\n
               \t'put the gold coin in the leather bag'\n\n
               You can create shortcuts to reduce typing; type 'alias' for 
               more details. Type 'width' to change the console's text width. 
               Type 'quit' to save your progress and leave 
               the game (NOTE: saving is not yet implemented)."""

    def __init__(self, net_conn, game = None):
        self.game = game
        self.user = None
        self.username = None
        self.raw_input = ''
        self.raw_output = ''
        self.change_players = False
        self.connection = net_conn
        self.width = Console.default_width
        self.tw = TextWrapper(width = self.width, replace_whitespace = False, drop_whitespace = True, tabsize = 4) 
        self.alias_map = {'n':       'go north',
                          's':       'go south',
                          'e':       'go east', 
                          'w':       'go west', 
                          'nw':      'go northwest',
                          'sw':      'go southwest',
                          'ne':      'go northeast',
                          'se':      'go southeast',
                          'u':       'go up',
                          'd':       'go down',
                          'i':       'inventory',
                          'l':       'look',
                          'x':       'execute'
                          }


    def detach(self, user):
        if self.user == user:
            self.user = None
        self.connection.send(b'Press Enter to continue . . . ')

    def set_width(self, w):
        self.width = w
        self.tw.width = w
    
    def get_width(self):
        return self.width
    
    def _add_alias(self, cmd):
        instructions = 'To create a new alias, type:\n    alias <a> <text>\n' \
                        'where <a> is the new alias and <text> is what will replace the alias.'
         
        if len(self.words) == 1:
            # print a list of current aliases & instructions for adding
            self.write('Current aliases:')
            for a in sorted(self.alias_map, key=self.alias_map.get):
                self.write('%s --> %s' % (a.rjust(12), self.alias_map[a]))
            self.write(instructions)
            return 
        alias = self.words[1]
        if len(self.words) == 2:
            # print the particular alias if it exists
            if (alias in self.alias_map):
                self.write("'%s' is currently aliased to '%s'" % (alias, self.alias_map[alias]))
            else:
                self.write("'%s' is not currently aliased to anything." % alias)
                self.write(instructions)
            return 
        # new alias specified, insert it into the alias_map
        if (alias in self.alias_map):
            self.write("'%s' is currently aliased to '%s'; changing." % (alias, self.alias_map[alias]))
        expansion = cmd.split(maxsplit=2)[2]    # split off first two words and keep the rest
        self.alias_map[alias] = expansion
        self.write("'%s' is now an alias for '%s'" % (alias, expansion))
        return

    def _replace_aliases(self):
        cmd = ""
        for t in self.words:
            if t in self.alias_map:
                cmd += self.alias_map[t] + " "
                dbg.debug("Replacing alias '%s' with expansion '%s'" % (t, self.alias_map[t]), 3)
            else:
                cmd += t + " "
        cmd = cmd[:-1]   # strip trailing space added above
        dbg.debug("User input with aliases resolved:\n    %s" % (cmd), 3)
        return cmd
    
    def _handle_console_commands(self):
        """Handle any commands internal to the console, returning True if the command string was handled."""
        if len(self.words) > 0:
            cmd = self.words[0]
            if cmd == 'alias':
                self._add_alias(self.command)
                return True
            
            if cmd == 'width': 
                if len(self.words) == 2 :
                    try: 
                        self.width = int(self.words[1])
                        self.write("Changing console width to %d" % self.width)
                    except ValueError:
                        self.write("Syntax error, changing console width to default %d." % self.default_width)
                        self.width = self.default_width
                    self.tw.width = self.width
                else:
                    self.write("The console width is currently %d. Type 'width <width>' to change it." % self.width)
                return True
            
            if cmd == 'help':
                self.write(self.help_msg)
                return True

            if cmd == 'debug':
                self.game.handle_exceptions = not self.game.handle_exceptions
                self.write("Toggle debug exception handling to %s" % ("on" if self.game.handle_exceptions else "off"))
                return True
            
            game_file_cmds = {'savegame':self.game.save_game,
                         'loadgame':self.game.load_game}
            if cmd in game_file_cmds:
                if (len(self.words) == 2):
                    filename = self.words[1]
                    game_file_cmds[cmd](filename)
                else:
                    self.write("Usage: %s <filename>" % cmd)
                return True
            if cmd == 'save':
                if (len(self.words) == 2):
                    filename = self.words[1]
                    self.game.save_player(filename, self.user)
                else:
                    self.write("Usage: save <filename>")
                return True
            if cmd == 'load':
                if (len(self.words) == 2):
                    filename = self.words[1]
                    try:
                        self.game.load_player(filename, self.user, self)
                    except gametools.PlayerLoadError:
                        self.write("Encountered an error trying to load from file.")
                else:
                    self.write("Usage: load <filename>")
                return True
        return False

    def write(self, text, indent=0):
        str_text = str(text)
        self.tw.initial_indent = indent * ' '
        self.tw.subsequent_indent = indent * ' '
        lines = str_text.splitlines()
        for l in lines: 
            wrapped = self.tw.fill(l)
            self.raw_output += wrapped + '\n'
        self.raw_output = self.raw_output.replace('\n','<br>').replace('\t', '&nbsp&nbsp&nbsp&nbsp')
        asyncio.ensure_future(connections_websock.ws_send(self))

    '''
    def new_user(self):
        self.write("Create your new user.")
        user_default_name = input("User default name: ")    #TODO: Simplify and make text more user-friendly.
        user_short_description = input("User short description: ")
        user_long_description = input("User long description: ")
        new_user = Player(user_default_name, self)
        new_user.set_description(user_short_description, user_long_description)
        new_user.set_max_weight_carried(750000)
        new_user.set_max_volume_carried(2000)
        new_user.move_to(self.user.location)
        for i in self.user.contents:
            i.move_to(new_user)
        self.write("You are now %s!" % new_user.id)
        self.user.move_to(Thing.ID_dict['nulspace'])
        self.user.cons = None
        self.set_user(new_user)
        self.game.user = new_user
    '''

    def take_input(self):
        if (self.raw_input == ''):
            return None
        (self.command, sep, self.raw_input) = self.raw_input.partition('\n')
        self.words = self.command.split()
        # if user types a console command, handle it and start over unless the player that called this is deactive
        internal = self._handle_console_commands()
        if internal:
            return "__noparse__"
        # replace any aliases with their completed version
        self.final_command = self._replace_aliases()
        return self.final_command
