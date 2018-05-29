import thing
import gametools
import action

class Plaque(thing.Thing):
    def __init__(self, mirror, number):
        super().__init__('plaque', __file__)
        self.set_description('stone plaque', 'Thou must intone the word that best describes thee.', unlisted=True)
        self.words = ['dark-eyed',
                      'green-eyed', 
                      'red-eyed',
                      'orange-eyed',
                      'blue-eyed',
                      'brown-eyed',
                      'black-eyed',
                      'violet-eyed',
                      'clear-eyed',
                      'young',
                      'old',
                      'short',
                      'tall',
                      'slender', 
                      'fat',
                      'heavy',
                      'thin',
                      'slim',
                      'swarthy', 
                      'pale',
                      'dark-skinned', 
                      'fair-haired',
                      'dark-haired',
                      'red-haired',
                      'short-haired',
                      'long-haired',
                      'bearded',
                      'languid',
                      'happy',
                      'melancholy',
                      'long-limbed'               
                      ] 
        self.mirror = mirror
        self.number = number
        self.actions.append(action.Action(self.intone, ['intone', 'acquire'], True, False))
        self.actions.append(action.Action(self.look_at, ['read'], True, False))

    def look_at(self, p, cons, oDO, oIDO):
        words_on_plaque = ''
        for i in self.words:
            words_on_plaque += i + '\n'
        cons.user.perceive('This plaque has a list of words on it. They read:\n<div style="column-count:3;column-rule:none">' + words_on_plaque + '</div>Below the list of words are some instructions. They read:\n' + self.long_desc)
        return True

    def intone(self, p, cons, oDO, oIDO):
        (sV, sDO, sPrep, sIDO) = p.diagram_sentence(p.words)
        if not sDO:
            return "You must intone something!"
        if sDO not in self.words:
            cons.user.perceive('You try to intone %s, but somehow just can\'t grasp it.' % sDO)
            return True
        if self.number == 1:
            self.mirror.adj1 = sDO
        elif self.number == 2:
            if cons.user.adj1 == sDO:
                cons.user.perceive('You try to intone %s, but it\'s already part of you.' % sDO)
                return True
            self.mirror.adj2 = sDO
        cons.write('You see the reflection in the mirror change slightly.')
        return True
