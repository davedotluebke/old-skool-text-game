import ai_creature

class  Acleð(ai_creature.AINPC):
    def __init__(self):
        prompt = "Your name is Acleð. You live in a small stone hut atop a mountain range. You were descending the mountain when a fearsome flying creature, black with red stripes under its wings, about the size of a large crow, but with a very sharp beak, attacked you. You fled, but you lost your small golden key and need help getting it back. I have just walked into the area where you are standing. You will begin by telling me you need my help."
        super().__init__('human', __file__, prompt=prompt, aggressive=1, movement=0)
        self.set_description('short human', 'A short human, with short brown hair.')
        self.add_adjectives('short')
        self.add_names('acleð', 'acled')
        self.set_combat_vars(40, 40, 20, 60)
        self.proper_name = "Acleð" 
        self.gender = 'female'
        self.forbid_room('domains.centrata.fields.road_five')
    
    def consider_given_item(self, item, giving_creature):
        if item.path == 'domains.centrata.mountain.key':
            #self.choices.append(self.move_around)
            self.scripts = []
            self.say("Thank you so much!")
            return True, "Acleð gratefully accepts the key."
        self.say(f"I'm looking for my key, not {item.get_short_desc(giving_creature, True)}.")
        return False, "Acleð declines the key."

def clone():
    return Acleð()
