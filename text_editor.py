import gametools

class TextEditor:
    def __init__(self):
        self.text = ''
        self.line = ''
        self.obj = None

    def console_recv(self, line):
    self.line = line
    self.run()

    def run(self):
        self.text += (self.line+'\n')
        if self.line == '^EOF':
        if '^EOF\n' in self.text:
        (head, sep, tail) = self.text.partition('^EOF\n')
        self.text = head
        self.obj.ed_output = self.text
    self.text = ''
     self.obj.handle_end()
