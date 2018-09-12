import re
from thing import Thing
from action import Action

class Book(Thing):
    #
    # SPECIAL METHODS (i.e __method__() format)
    #
    def __init__(self, default_name, path, s_desc, l_desc, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description(s_desc, l_desc)
        self.book_pages = dict()
        self.add_names('book')
        self.cons = None
        self.COVER_INDEX = -1
        self.TOC_INDEX = 0
        # books always open on cover the first time and toc or bookmark afterwards
        self.index = self.COVER_INDEX 
        self.bookmark = None

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

        for line_text in message.splitlines(True):
            if line_text.strip(' \t\r\n') == "#*": 
                ## page break ##
                page_text += '\n\n'
                self.book_pages[int(index)] = page_text
                page_text = '\n'
                index += 1
                continue
            page_text += line_text 
        
        page_text += '\n\n'
        self.book_pages[index] = page_text

    #
    # OTHER EXTERNAL METHODS (misc externally visible methods)
    #
    def console_recv(self, input_string):

        command = input_string.lower().strip()

        cover_vocab = ["c", "cover", "front", "sleeve", "title", "author"]
        toc_vocab = ["toc", "table", "contents", "table of contents", "chapters", "index", "list"]
        next_vocab = ["n", "next", "next page", "turn page", "forward", "right", "continue", "go ahead", "go forward"]
        prev_vocab = ["p", "prev", "previous", "go back", "back", "backward", "left"]
        bookmark_vocab = ["b", "bookmark", "bookmark page", "mark", "mark page", "tag", "tag page", "fold", "fold corner", "earmark", "earmark page", "dogear", "dogear page", "dog-ear", "dog-ear page"]
        quit_vocab = ["q", "quit", "quit reading", "end", "stop", "stop reading", "exit", "leave", "close", "close book", "shut", "shut book", "put away"]

        # perform requested command
        if command in cover_vocab:
            # view cover
            self._set_index(self.COVER_INDEX)

            if not self.book_pages[self.COVER_INDEX]:
                self.cons.user.perceive("The cover is blank")
                return False

            self.cons.user.emit("&nD%s closes the %s and gazes at the cover." %(self.cons.user.id, self.short_desc))

        elif command in toc_vocab:
            # view table of contents
            last_index = self.index
            self._set_index(self.TOC_INDEX)

            if not self.book_pages[self.TOC_INDEX]:
                self.cons.user.perceive("This book has no table of contents.")
                return False

            if last_index == self.COVER_INDEX:
                self.cons.user.emit("&nD%s opens the %s and starts reading." %(self.cons.user.id, self.short_desc))
            else:
                self.cons.user.emit("&nD%s flips through the pages of the %s with a thoughtful expression." %(self.cons.user.id, self.short_desc))

        elif command in next_vocab:
            # view next page
            if not self._adjust_index(1):
                self.cons.user.perceive("You've reached the end.")
                return False

            if self.index == self.TOC_INDEX:
                self.cons.user.emit("&nD%s opens the %s and starts reading." %(self.cons.user.id, self.short_desc))
            else:
                self.cons.user.emit("&nD%s turns the page." %(self.cons.user.id))

        elif command in prev_vocab:
            # view next page
            if not self._adjust_index(-1):
                self.cons.user.perceive("You've reached the beginning.")
                return False

            if self.index == self.COVER_INDEX:
                self.cons.user.emit("&nD%s closes the %s and gazes at the cover." %(self.cons.user.id, self.short_desc))
            else:
                self.cons.user.emit("&nD%s turns back a page." %(self.cons.user.id))
        
        elif command in bookmark_vocab:
            # toggle bookmark
            if self.bookmark == self.index:
                if self.bookmark == self.COVER_INDEX:
                    self.cons.user.perceive("You decide that the cover isn't so important after all.")
                else:
                    self.cons.user.perceive("You unmark the page.")
                    self.cons.user.emit("&nD%s smooths out the page." %(self.cons.user.id))

                self.bookmark = None
            else:
                self.bookmark = self.index
                
                if self.bookmark == self.COVER_INDEX:         
                    self.cons.user.perceive("You make a mental note to examine this cover later.")
                    self.cons.user.emit("&nD%s stares intently at the cover." %(self.cons.user.id))
                else:
                    self.cons.user.perceive("You dog-ear the page for later.")
                    self.cons.user.emit("&nD%s dog-ears the page." %(self.cons.user.id))
            
        elif command in quit_vocab: 
            # stop input_takeover
            self.index = self.bookmark or self.TOC_INDEX
            self.cons.input_redirect = None
            self.cons.user.perceive("You put the %s away." %(self.short_desc))
            self.cons.user.emit("&nD%s puts the %s away." %(self.cons.user.id, self.short_desc))
            self.cons = None
            return False

        elif command.isdigit():
            # select page by number
            if not self._set_index(command):
                self.cons.user.perceive("You can't find that page.")
                return False

            self.cons.user.emit("&nD%s flips through the pages of the %s with a thoughtful expression." %(self.cons.user.id, self.short_desc))

        else:
            self.cons.user.perceive("Other actions are blocked while reading; type 'quit' to exit reading mode.")

        # output selected page and available commands
        if self.index == self.COVER_INDEX:
            self.cons.write("\nThe cover reads:", 4)
        elif self.index == self.TOC_INDEX:
            self.cons.write("\nTable of Contents:", 4)
        else:
            self.cons.write("\nPage %s:" %self.index, 4)

        command_list = "Commands: (C)over  (TOC)  (N)ext  (P)revious  (B)ookmark  (Q)uit"
        if self.index == self.bookmark:
            command_list = command_list.replace("(B)", "[B]");

        self.cons.write("%s" % self.book_pages[self.index], 8)
        ##self.cons.user.perceive("\nYou are reading the &nd%s...\n\n" %self.id)
        self.cons.user.perceive("%s" %command_list)
        self.cons.user.perceive("          [Type a page number to read it.]\n\n")

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
        directly to self.console_recv() via the input takeover system
        '''
        if self not in cons.user.contents:
            cons.write('You need to take the book before reading it!')
            return True

        # take over user input
        cons.request_input(self)
        self.cons = cons
        
        if self.index == self.COVER_INDEX:
            self.cons.user.emit("&nD%s takes out a %s and looks at the cover." %(self.cons.user.id, self.short_desc))
        else:
            self.cons.user.emit("&nD%s opens a %s and starts reading." %(self.cons.user.id, self.short_desc))

        # show the last page read when book is opened
        self.console_recv("")

        return True

    def close(self, p, cons, oDO, oIDO):
        # the book is always closed because this verb action is 
        # unavailable while in takeover reading mode
        cons.write("It's already closed.")
        return True

    actions = dict(Thing.actions)  # make a copy, don't change Thing's dict!
    actions['read'] =  Action(read, True, False)
    actions['open'] =  Action(read, True, False))
    actions['close'] = Action(close, True, False)
