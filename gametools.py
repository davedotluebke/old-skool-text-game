import os

gameroot = os.path.dirname(__file__) 

def initGameTools():
    '''Call this once after the game has started but before any code
    using gametools has been run.  Assumes gametools.py lives at the 
    root of the game source tree.'''
    # global gameroot
    pass

def findGamePath(filepath):
    gamePath = os.path.relpath(filepath, gameroot).replace("\\", ".").replace("/", ".")
    (head, sep, tail) = gamePath.partition(".py")
    gamePath = head
    return gamePath
