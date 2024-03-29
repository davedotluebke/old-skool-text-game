import creature

class  Acleð(creature.NPC):
    def __init__(self):
        super().__init__('human', __file__, aggressive=1, movement=0)
        self.set_description('short human', 'A short human, with short brown hair.')
        self.add_adjectives('short')
        self.add_names('acleð', 'acled')
        self.set_combat_vars(40, 40, 20, 60)
        self.proper_name = "Acleð" 
        self.gender = 'non-binary'

        self.add_script("Please, will you help me?")
        self.affirmative_responses = ['yes', 'ok', 'okay', 'of course']
        self.negative_responses = ['no']
        self.inquiry_responses = ['maybe', 'what', 'how']

        self.current_stage = 0
        self.explanation = """Thank you! I am Acleð and let me explain my perdicament.
        I was descending the mountain to purchase some bread when this giant flying creature dove at me.
        I ran to take shelter and thought I had fended it off, but when I returned to my hut I realised that my small golden key was gone.
        I believe the flying creature stole it and I need help retrieving it."""

        self.future_movement_path = ["west", "west", "west", "west", "north"]

    def perceive(self, message):
        super().perceive(message)

        affirmed = False
        denied = False
        inquired = False

        for i in self.affirmative_responses:
            if i in message:
                affirmed = True
        
        for i in self.negative_responses:
            if i in message:
                denied = True

        for i in self.inquiry_responses:
            if i in message:
                inquired = True

        if affirmed and denied:
            self.say("What? I didn't understand you.")
            return
        
        if affirmed or inquired:
            if self.current_stage == 0:
                self.current_script = self.explanation
                self.current_stage = 1
                if affirmed:
                    self.scripts = ["I'm awaiting someone who offered to help me."]
                for obj in self.location.contents: # introduce self as will explain in script next turn
                    if isinstance(obj, creature.Creature) and obj != self:
                        try:
                            obj.introduced.add(self.id)
                        except AttributeError: # XXX fix set save/restore code instead of this hack
                            obj.introduced = set(obj.introduced)
                            obj.introduced.add(self.id)
            elif self.current_stage == 1:
                if affirmed:
                    self.say("Thank you so much! That would be wonderful.")
                if inquired:
                    self.say("Let me explain again.")
                    self.current_script = self.explanation
            
        elif denied:
            self.say("Please, I beg of you! Help me!")
    
    def consider_given_item(self, item, giving_creature):
        if item.path == 'domains.centrata.mountain.key':
            #self.choices.append(self.move_around)
            self.scripts = []
            self.say("Thank you so much!")
            self.movement_path = self.future_movement_path
            self.choices.append(self.follow_path)
            return True, "Acleð gratefully accepts the key."
        self.say(f"I'm looking for my key, not {item.get_short_desc(giving_creature, True)}.")
        return False, f"Acleð declines the {item.get_short_desc(giving_creature, True)}."

def clone():
    return Acleð()
