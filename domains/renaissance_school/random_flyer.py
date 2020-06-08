import thing
import random
import action

class Flyer(thing.Thing):
    def __init__(self, default_name, path, message, pref_id=None, plural_name=None):
        super().__init__(default_name, path, pref_id=pref_id, plural_name=plural_name)
        self.messsage = message
    
    def read(self, p, cons, oDO, oIDO):
        cons.user.perceive("On this flyer you read: ")
        cons.user.perceive(self.messsage)
        return True
    
    def look_at(self, p, cons, oDO, oIDO):
        value = super().look_at(p, cons, oDO, oIDO)
        if value != True:
            return value
        return self.read(p, cons, oDO, oIDO)
    
    actions = dict(thing.Thing.actions)
    actions['look'] = action.Action(look_at, True, False)
    actions['examine'] = action.Action(look_at, True, False)
    actions['read'] = action.Action(read, True, False)


flyer_contents = [
    # format: short description, long description, adjectives (list), message
    # TODO: accurate flyer messages
    ("white and green flyer", "This flyer is white and green in colour.", ["white", "green"], "## Renaissance School Open House\n"
    "Our annual open house will be occuring on the 5th of November. "
    "Prospective students are encouraged to visit us. We will have a "
    "special performance by the music ensemble and a special suprise "
    "by the business class. "),
    ("picture-covered flyer", "This flyer has many pictures on it.", 
    ["picture", "covered", "picture-covered"], "## Bring a friend\n"
    "Our annual bring a friend day will be occuring on the 6th of November. "
    "All students are invited to bring their friends to visit for the "
    "day. Visitors must be registered with the front office. For more "
    "details, please visit our website: [https://www.renaissanceschool.org]"
    "(https://www.renaissanceschool.org)"),
    ("blue and white flyer", "This flyer is blue and white.", 
    ["blue", "white"], "## The Road to College\n"
    "Are you unsure about your child's steps through high school? "
    "Sara C Johnson, head of Renaissance School and college consuling "
    "expert will help explain the proccess to you in one of her workshops. "
    "Unfortunately, the person who wrote this flyer does not know "
    "when and where the workshop is occuring, so that information has "
    "not been included. "),
    ("red, orange, and yellow flyer", "This flyer is a dull red, a bright "
    "orange, and a pale yellow. ", ["red", "orange", "yellow", "dull", "bright", 
    "pale"], "## Summer programs at Virginia Variety University\nVirgina Variety "
    "University is happy to announce that our summer programs will be occuring "
    "this year. We are offering specialised courses for students who "
    "want to go more in depth in a subject area than is possible durring the "
    "school year. These programs have been specially designed to engage more "
    "than one subject area. Among our many offerings this year are such diverse "
    "elements as:\n- Engineering and Computing: Using 3D modeling software, students "
    "will design devices to reverse the rotation of the earth\n- Roman Muralism: "
    "Students will travel to Pompeii and assist in excavations of Roman murals. "
    "Students will then create their own mural in the same style. \n- The History of "
    "the Universe: Students will study the history of the universe, up to 2012, with "
    "a focus on crickets. \n- Ocean Studies: Students will spend the first week at sea, "
    "and will transcribe the sound of the sea onto sheet music. The students will "
    "then perform this music at the end of the second week. \n\nAll of our summer "
    "programs, with the exception of Ocean Studies, will occur on our campus "
    "in North Garden, Virginia. Students will stay on campus in the dorms "
    "for the duration of the summer programs. \n\n**Special Request: Due to "
    "some shortages, students with computers able to run 3D modeling software are "
    "encouraged to bring them. Please note that the software requires "
    "Windows Vista or Windows XP.**"),
    ("beige flyer", "This flyer is a plain beige colour with a dodecahedron on top.",
    ["beige", "plain", "dodecahedron"], "## Renaissance School\n#### College "
    "preperatory high school\nRenaissance School is a college preperatory "
    "high school with a focus on multiplidiscenary education. "
    "Founded in 1999, Renaissance School has provided 20 years "
    "of excelent education to Charlottesville and surrounding "
    "communities. For more information please visit [our website](https://www.renaissanceschool.org).")
]

def clone():
    fcc = random.choice(flyer_contents)
    f = Flyer('flyer', __file__, fcc[3])
    f.set_description(fcc[0], fcc[1])
    f.add_adjectives(*fcc[2])
    return f
