import domains.school.sink as sinkMod

def clone():
        
    sink = sinkMod.Sink('sink', __file__)
    sink.add_adjectives('metal', "60's")
    return sink

