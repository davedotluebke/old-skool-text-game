# At the beginning of the file, we need to import the modules we are going to use
# 
# Since the feather cannot contain anything or move on its own, we leave it as a 
# simple thing
# 
# The lowercase module 'thing' is the file where the uppercase class 'Thing' is found.
from thing import Thing

# The clone function is the function that is called when an object is created. In a 
# simple object such as this one, all code except the import statement at the top
# will be in this function. The function should not take any paramaters.
def clone():
  	# in Python, blocks of code such as functions are indicated by indents
   	
    # Objects are initialized by calling the class constructor and putting the value
    # returned into a variable. The variable name is only used in this file, but
    # making it something descriptive can help make the file easier to understand.
    # The second paramater to the constructor should always be '__file__'. This is
    # used internally to help the object's filepath be recorded.
    feather = Thing('feather', __file__)
    #  ^        ^      ^           ^
    # variable class name filepath (automatically calculated)
    
    # Once we have created the object, we can call functions on it to add features 
    # and description. Here we call the set_description function to add a short and 
    # long description. The short description is what we see of the object if it is
    # being listed in where it is located. The long description is what we see if 
    # we type 'look [object]'.
    feather.set_description('blue feather', 'This light blue feather is smooth and soft. It looks like it could be used as a pen.')
    #  ^          ^               ^                         ^
    # variable   function  short description         long description
    
    # We can add adjectives to the object to let players more easily differentiate it
    # from other similar objects. Normally the list of adjectives should include every
    # adjective that is used to describe the object in the descriptions. You can include
    # as many adjectives as you would like, separated by commas.
    feather.add_adjectives('blue', 'light', 'smooth', 'soft')
    #   ^         ^                     ^
    # variable function             adjectives
    
    # If we think someone might refer to the object by another name, you can add names
    # so the game code can figure out what they mean. In this case, someone might
    # refer to the feather as a quill or a pen, so we can add those names here.
    feather.add_names('quill', 'pen')
    
    # We can set the object's weight and volume here. The weight of objects is specified
    # in grams and the volume in liters. Since feathers are incredibly light, we 
    # will only give it a weight of 1 gram. However, for many objects this value
    # will be much larger.
    feather.set_weight(1)
    feather.set_volume(0.1)
    
    # If the object is worth anything, we can set a value of the object. A value of
    # 1 is equivalent to the value of a copper coin.
    feather.set_value(30)
    
    # At the end of the clone function we need to return the object. If we fail to
    # return the object, we will never be able to access it. Don't forget this step!
    return example
