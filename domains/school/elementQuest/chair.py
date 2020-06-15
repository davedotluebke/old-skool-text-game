import gametools
import scenery

def clone():
    chair = scenery.Scenery('chair', 'wooden chair', 'This wooden chair is behind the desk.', unlisted=True)
    chair.add_adjectives('wooden', 'desk')
    chair.add_response(['sit'], 'You sit in the chair and it creaks as you do.')
    chair.add_response(['stand'], 'You stand up and it creacks agian.', False, True)

    return chair