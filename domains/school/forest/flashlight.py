import domains.school.flashlight as flashlightMod

def clone():
    flashlight = flashlightMod.Flashlight('flashlight', __file__)
    flashlight.set_description('old flashlight', 'An old metal flashlight.')
    return flashlight
