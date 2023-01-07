# In this file, we are going to create a container to put our feather into
# First we are going to import the Container class from the module container
# Containers are like things, except they can contain other things
from container import Container

# the clone function for Containers function identically to Things 
def clone():
    # the format for creating Containers is the same as for Things,
    # except using 'Container' rather than 'Thing'
    bag = Container('bag', __file__)
    bag.set_description('leather bag', 'This battered leather bag looks like it has seen heavy use.')
    bag.add_adjectives('battered', 'leather', 'worn')
    bag.set_weight(1000) # don't forget that weight is in grams, not kilograms
    bag.set_volume(10)
    # In addition to everything that Things can do, Containers can have a max
    # weight and max volume carried. This value defaults to 0, so you should
    # make sure to change it.
    bag.set_max_weight_carried(20000)
    bag.set_max_volume_carried(10)
    # if the container can be opened and closed, you should set the 'closeable'
    # attribute to True.
    bag.closable = True
    return bag