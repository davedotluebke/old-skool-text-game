import re
from thing import Thing
from action import Action

class Book(Thing):
    def __init__(self, default_name, path, s_desc, l_desc, pref_id=None):
        super().__init__(default_name, path, pref_id)
        self.set_description(s_desc, l_desc)
        self.what_you_read = list()
        self.index = 0
        self.actions.append(Action(self.read, ['read'], True, False))
        self.add_names('book')

    def set_message(self, message):
        self.what_you_read = list()
        page_text = '\n'

        for line_text in message.splitlines(True):
            if line_text.strip(' \t\r\n') == "#*": 
                ## page break ##
                self.what_you_read.append(page_text)
                page_text = '\n'
                continue
            page_text += line_text 

        self.what_you_read.append(page_text + '\n\n')

    def read(self, p, cons, oDO, oIDO):
        '''
            case == 1: read current page
            case == 2: read specific page
            case == 3: read next page
        '''
        if self not in cons.user.contents:
            cons.write('You need to take the book before reading it!')
            return True
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        case = None
        if oDO == self:
            if cons.user.reading:
                case = 3
            else:
                case = 1

        if not case:
            # search the direct object string (sDO) to determine which page to read
            match = re.search(r'page (\d+)', sDO)
            if match:
                #> read page #
                pagenum = match.group(1)
                case = 2
            elif re.search(r'next page', sDO):
                #> read next page
                case = 3
            elif re.search(r'page', sDO):
                #> read page
                case = 1
            else:
                match = re.search(r'(\S+)', sDO)

                if match and match.group(1) in self.names:
                    #> read [this book's name]
                    case = 1
        try:
            can_read = True

            # select the appropriate page to read
            if not self.what_you_read:
                # there's nothing to read
                can_read = False
                cons.write("It appears to be blank...")
                cons.user.emit("&nD%s stares confusedly at the %s." %(cons.user.id, self.short_desc))
            elif (case == 2):
                if 0 < int(pagenum) <= len(self.what_you_read):
                    if (self.index != int(pagenum)-1):
                        # not the same page as last time
                        self.index = int(pagenum)-1
                        cons.write('You flip to page ' + str(self.index+1) + '.')
                else:
                    raise IndexError
            elif (case == 3):
                if (self.index+1 == len(self.what_you_read)):
                    can_read = False
                else: 
                    self.index += 1

            if can_read:
                cons.write("You read:" + str(self.what_you_read[self.index]), 8)
                if not cons.user.reading:
                    cons.user.emit("&nD%s opens the %s and starts to read." %(cons.user.id, self.short_desc))
                else:
                    cons.user.emit("&nD%s flips through the pages of the %s thoughtfully." %(cons.user.id, self.short_desc))
                cons.user.reading = True
            elif not self.what_you_read:
                # blank book
                cons.write("It appears to be blank...")
                cons.user.emit("&nD%s stares confusedly at the %s." %(cons.user.id, self.short_desc))
            else:
                # end of book
                cons.write("There's nothing left to read.")

        except IndexError:
            cons.write("You can't seem to find that page...")
        return True
