import thing
import text_editor

class TextEditorUseExample(thing.Thing):
    def __init__(self):
        super().__init__('paper', __file__)
        self.set_description('paper', 'This is a paper you can write on.')
        self.text_on = ''
        self.text_editor = text_editor.TextEditor()
        self.actions.append(thing.Action(self.read, ['read'], True, True))
        self.actions.append(thing.Action(self.write, ['write'], True, True))
        self.text_editor.obj = self
        self.cons = None
        self.ed_output = ''

    def read(self, p, cons, oDO, oIDO):
        cons.user.perceive("You read: " + self.text_on)
        return True

    def write(self, p, cons, oDO, oIDO):
        cons.user.perceive("You begin writing on the paper. Type ^EOF to finish.")
        cons.request_input(self.text_editor)
        self.cons = cons
        return True

    def handle_end(self):
        self.cons.input_redirect = None
        self.cons.user.perceive("You finish writing on the paper and look up.")
        self.cons = None
        self.text_on = self.ed_output

def clone():
    return TextEditorUseExample()