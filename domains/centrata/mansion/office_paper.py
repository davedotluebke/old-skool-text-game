import thing

def clone():
    paper = thing.Thing('paper', __file__)
    paper.set_description('piece of paper', 'This is a piece of paper.', p_s_desc='pieces of paper')
    paper.add_adjectives('piece')
    paper.accepts_writing = True
    return paper
