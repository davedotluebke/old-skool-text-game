import creature
import player
import game_openai

GAME_WIDE_PROMPT = "Let's begin a conversation where you respond in the style of an NPC in a text adventure game. Give only the bare lines of dialogue, with no quotes or other formatting. The setting is a mediaeval-esque fantasy world. If the answer is not obvious from this first prompt, you should respond that you do not know about the topic."

class AINPC(creature.NPC):
    def __init__(self, ID, path, prompt, aggressive=0, movement=1, pref_id=None):
        super().__init__(ID, path, aggressive, movement, pref_id)
        self.prompt = GAME_WIDE_PROMPT + prompt
        self.current_conversation = ""
        self.choices.remove(self.talk) # remove the default "talk" option, replacing it with a fancier version
        self.choices.remove(self.do_act) # similar

    def set_prompt(self, new_prompt):
        self.prompt = GAME_WIDE_PROMPT + new_prompt
    
    def perceive(self, message, force=False):
        formatted_message = player.Player.perceive(self, message, silent=True, force=force)

        self.current_conversation += formatted_message
        self.current_conversation += ':\n'

        response = game_openai.openai_completion(self.prompt + self.current_conversation)
        self.log.info(f"raw message: {message}\nformatted message: {formatted_message}\nprompt: {self.prompt + self.current_conversation}\nresponse: {response}")
        
        self.say(response)

