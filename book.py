import re
from thing import Thing
from action import Action

class Book(Thing):
    def __init__(self, default_name, s_desc, l_desc, pref_id=None):
        super().__init__(default_name, pref_id)
        self.set_description(s_desc, l_desc)
        self.what_you_read = list()
        self.index = 0
        self.actions.append(Action(self.read, ['read'], True, False))
        self.add_names('book')

    def set_message(self, message):
        page_num = 0
        c = 0
        page = '\n'
        for i in message.splitlines(True):
            if i == "#*\n":
                page_num += 1
                c = 0
                try:
                    self.what_you_read[page_num] = page
                except IndexError:
                    self.what_you_read.append(page)
                page = '\n'
                continue
            page += i
            c += 1
            # #* means page break
        try:
            self.what_you_read[page_num] = (page + '\n\n')
        except IndexError:
            self.what_you_read.append(page + '\n\n')

    def read(self, p, cons, oDO, oIDO):
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
        # see if they typed "read page #" 
        match = re.search(r'page (\d+)', sDO)
        if match:
            pagenum = match.group(1)
            case = 2
        if not case:
            match = re.search(r'next page', sDO)
            if match:
                case = 3
            if not case:
                match = re.search(r'page', sDO)
                if match:
                    case = 1
                if not case:
                    match = re.search(r'(\S+)', sDO)
                    if match:
                        if match.group(1) in self.names:
                            case = 1
        try:
            if self.what_you_read and (case == 1):
                cons.write("You read:"+str(self.what_you_read[self.index]), 8)
                cons.user.reading = True
                return True
            elif self.what_you_read and (case == 2):
                self.index = int(pagenum)-1
                cons.write('You flip to page '+str(self.index+1)+'.')
                cons.write("You read:"+str(self.what_you_read[self.index]), 8)
                cons.user.reading = True
                return True
            elif self.what_you_read and (case == 3):
                self.index += 1
                cons.write("You read:"+str(self.what_you_read[self.index]), 8)
                cons.user.reading = True
                return True
            else:
                cons.write("A problem occured!")
                return True
        except IndexError:
            cons.write('The book does not have a page numbered %s!' % str(self.index+1))
            return True
