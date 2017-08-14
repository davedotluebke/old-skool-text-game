import room
import scenery
import gametools

def load():
    roomPath = gametools.findGamePath(__file__)
    exists = room.check_loaded(roomPath)
    if exists: return exists

    shack = room.Room('shack', roomPath)
    shack.set_description('empty shack', 'This shack appears to be abandoned and has nothing but cobwebs and walls.')
    shack.add_exit('out', 'domains.school.forest.field')
    
    rake = scenery.Scenery("rake","broken rake", "This rake looks like it broke a long time ago.")
    rake.add_adjectives("broken")
    rake.add_response(["get","take"], "When you lean down to take it one of the tines pokes you in the eye. Ow! ", emit_message='%s reaches to take the rake, and stops.')
    rake.add_response(["rake", "use"],"You can not reach the handle.")
    shack.insert(rake)

    return shack