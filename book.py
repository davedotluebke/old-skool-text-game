import re
import gametools
from thing import Thing
from action import Action
import json

class Book(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, s_desc, l_desc, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description(s_desc, l_desc)
        self.book_pages = dict()
        self.spells = {}
        self.add_names('book')
        self.current_reader = None
        self.COVER_INDEX = -1
        self.TOC_INDEX = 0
        # books always open on cover the first time and toc or bookmark afterwards
        self.index = self.COVER_INDEX 
        self.bookmark = None
        self.versions[gametools.findGamePath(__file__)] = 1

    #
    # INTERNAL USE METHODS (i.e. _method(), not imported)
    #
    def _set_index(self, new_index):
        if int(new_index) in self.book_pages:
            self.index = int(new_index)
            return True

        return False
    
    def _adjust_index(self, adjustment):
        return self._set_index(self.index + adjustment)

    #
    # SET/GET METHODS (methods to set or query attributes)
    #
    def set_message(self, message):
        self.book_pages = {self.COVER_INDEX:"", self.TOC_INDEX:""}
        page_text = '\n'
        index = self.COVER_INDEX
        self.spells[index] = {}

        for line_text in message.splitlines(True):
            if line_text.strip(' \t\r\n') == "#*": 
                ## page break ##
                page_text += '\n\n'
                self.book_pages[int(index)] = page_text
                page_text = '\n'
                index += 1
                self.spells[index] = {}
                continue
            if line_text.lstrip().startswith('\0'):
                ## spell on page ##
                line_text = line_text.lstrip()[1:]
                try:
                    spells_on_page = json.loads(line_text)
                except Exception as e:
                    self.log.error(e)
                else:
                    self.spells[index] = spells_on_page
                continue
            else:
                page_text += line_text 
        
        page_text += '\n\n'
        self.book_pages[index] = page_text

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def accept_command(self, input_string):

        command = input_string.lower().strip()

        cover_vocab = ["c", "cover", "front", "sleeve", "title", "author"]
        toc_vocab = ["toc", "table", "contents", "table of contents", "chapters", "index", "list"]
        next_vocab = ["n", "next", "next page", "turn page", "forward", "right", "continue", "go ahead", "go forward"]
        prev_vocab = ["p", "prev", "previous", "go back", "back", "backward", "left"]
        bookmark_vocab = ["b", "bookmark", "bookmark page", "mark", "mark page", "tag", "tag page", "fold", "fold corner", "earmark", "earmark page", "dogear", "dogear page", "dog-ear", "dog-ear page"]
        learn_vocab = ["l", "learn", "memorize", "memorise"]
        quit_vocab = ["q", "quit", "quit reading", "end", "stop", "stop reading", "exit", "leave", "close", "close book", "shut", "shut book", "put away"]

        # perform requested command
        if command in cover_vocab:
            # view cover
            self._set_index(self.COVER_INDEX)

            if not self.book_pages[self.COVER_INDEX]:
                self.current_reader.perceive("The cover is blank")
                return False

            self.current_reader.emit("&nD%s closes the %s and gazes at the cover." %(self.current_reader.id, self._short_desc))

        elif command in toc_vocab:
            # view table of contents
            last_index = self.index
            self._set_index(self.TOC_INDEX)

            if not self.book_pages[self.TOC_INDEX]:
                self.current_reader.perceive("This book has no table of contents.")
                return False

            if last_index == self.COVER_INDEX:
                self.current_reader.emit("&nD%s opens the %s and starts reading." %(self.current_reader.id, self._short_desc))
            else:
                self.current_reader.emit("&nD%s flips through the pages of the %s with a thoughtful expression." %(self.current_reader.id, self._short_desc))

        elif command in next_vocab:
            # view next page
            if not self._adjust_index(1):
                self.current_reader.perceive("You've reached the end.")
                return False

            if self.index == self.TOC_INDEX:
                self.current_reader.emit("&nD%s opens the %s and starts reading." %(self.current_reader.id, self._short_desc))
            else:
                self.current_reader.emit("&nD%s turns the page." %(self.current_reader.id))

        elif command in prev_vocab:
            # view next page
            if not self._adjust_index(-1):
                self.current_reader.perceive("You've reached the beginning.")
                return False

            if self.index == self.COVER_INDEX:
                self.current_reader.emit("&nD%s closes the %s and gazes at the cover." %(self.current_reader.id, self._short_desc))
            else:
                self.current_reader.emit("&nD%s turns back a page." %(self.current_reader.id))
        
        elif command in bookmark_vocab:
            # toggle bookmark
            if self.bookmark == self.index:
                if self.bookmark == self.COVER_INDEX:
                    self.current_reader.perceive("You decide that the cover isn't so important after all.")
                else:
                    self.current_reader.perceive("You unmark the page.")
                    self.current_reader.emit("&nD%s smooths out the page." %(self.current_reader.id))

                self.bookmark = None
            else:
                self.bookmark = self.index
                
                if self.bookmark == self.COVER_INDEX:         
                    self.current_reader.perceive("You make a mental note to examine this cover later.")
                    self.current_reader.emit("&nD%s stares intently at the cover." %(self.current_reader.id))
                else:
                    self.current_reader.perceive("You dog-ear the page for later.")
                    self.current_reader.emit("&nD%s dog-ears the page they are on." %(self.current_reader.id))
        
        elif command.startswith(tuple(learn_vocab)):
            if self.spells[self.index] == {}:
                self.current_reader.perceive("You don't see any spells on the page that you could learn.")
            elif command.partition(" ")[2] in self.spells[self.index]:
                spell_name = command.partition(" ")[2]
                spell_path = self.spells[self.index][spell_name]
                if spell_name in self.current_reader.spellsKnown:
                    if self.current_reader.spellsKnown[spell_name] == spell_path:
                        self.current_reader.perceive("You already know that spell!")
                        return False
                    else:
                        self.current_reader.perceive("You relearn the %s spell from the page." % spell_name)
                else:
                    self.current_reader.perceive("You learn the %s spell from the page." % spell_name)
                self.current_reader.spellsKnown[spell_name] = spell_path
            else:
                self.current_reader.perceive("There seems to be a spell on the page, but not one named %s." % command.partition(" ")[2])
            return False
            
        elif command in quit_vocab: 
            # stop input_takeover
            self.index = self.bookmark or self.TOC_INDEX
            self.current_reader.message_target = Thing.game.parser
            self.current_reader.perceive("You put the %s away." %(self._short_desc))
            self.current_reader.emit("&nD%s puts the %s away." %(self.current_reader.id, self._short_desc))
            self.cons = None
            return False

        elif command.isdigit():
            # select page by number
            if not self._set_index(command):
                self.current_reader.perceive("You can't find that page.")
                return False

            self.current_reader.emit("&nD%s flips through the pages of the %s with a thoughtful expression." %(self.current_reader.id, self._short_desc))

        else:
            self.current_reader.perceive("Other actions are blocked while reading; type 'quit' to exit reading mode.")

        # output selected page and available commands
        if self.index == self.COVER_INDEX:
            self.current_reader.perceive("\nThe cover reads:", 4)
        elif self.index == self.TOC_INDEX:
            self.current_reader.perceive("\nTable of Contents:", 4)
        else:
            self.current_reader.perceive("\nPage %s:" %self.index, 4)

        command_list = "Commands: (C)over  (TOC)  (N)ext  (P)revious  (B)ookmark  (L)earn \\[spell\\]  (Q)uit"
        if self.index == self.bookmark:
            command_list = command_list.replace("(B)", "[B]")

        self.current_reader.perceive("%s" % self.book_pages[self.index], 8)
        ##self.current_reader.perceive("\nYou are reading the &nd%s...\n\n" %self.id)
        self.current_reader.perceive("%s" %command_list)
        self.current_reader.perceive("          [Type a page number to read it.]\n\n")

        return True

    #
    # ACTION METHODS & DICTIONARY (dictionary must come last)
    #
    
    def drop(self, p, cons, oDO, oIDO):
        # make it so the next person to pick up the book doesn't start 
        # reading where the last left off
        self.index = self.COVER_INDEX
        self.bookmark = None

        return super(Book, self).drop(p, cons, oDO, oIDO)
    def read(self, p, cons, oDO, oIDO):
        '''
        This function is only executed when reading starts. All subsequent actions are sent 
        directly to self.accept_command() by changing the user's message target.
        '''

        if self not in cons.user.contents:
            cons.user.perceive('You need to take the book before reading it!')
            return True
        
        if oDO != self:
            return "Did you mean to read a book?"

        # take over user input
        self.current_reader = cons.user
        self.current_reader.message_target = self
        
        if self.index == self.COVER_INDEX:
            self.current_reader.emit("&nD%s takes out a %s and looks at the cover." %(self.current_reader.id, self._short_desc))
        else:
            self.current_reader.emit("&nD%s opens a %s and starts reading." %(self.current_reader.id, self._short_desc))

        # show the last page read when book is opened
        self.accept_command("")

        return True

    def close(self, p, cons, oDO, oIDO):
        # the book is always closed because this verb action is 
        # unavailable while in takeover reading mode
        cons.user.perceive("It's already closed.")
        return True

    actions = dict(Thing.actions)  # make a copy, don't change Thing's dict!
    actions['read'] =  Action(read, True, False)
    actions['open'] =  Action(read, True, False)
    actions['close'] = Action(close, True, False)
