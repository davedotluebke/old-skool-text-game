import gametools

def run():
    text = ''
    line = ''
    while True:
        line = input(':')
        text += (line+'\n')
        if line == '^EOF':
            break
    if '^EOF\n' in text:
        (head, sep, tail) = text.partition('^EOF\n')
        text = head
    return text
