from random import choice

CHOICE_START = r'[rchoice]'
CHOICE_END = r'[/rchoice]'
CHOICE_SEP = r'[rsep]'

def choose(text):
    def consume_whitespace():
        nonlocal i, text
        ws = 0
        while i + ws < len(text) and text[i + ws].isspace():
            ws += 1
        text = text[:i] + text[i+ws:]

    def consume_whitespace_pre():
        nonlocal i, text

        ws = 0
        while text[i - ws - 1].isspace():
            ws += 1
        # if started with space, keep that space
        if text[i - ws] == ' ':
            ws -= 1
        text = text[:i - ws] + text[i:]
        i -= ws

    def consume_whitespace_post():
        # if ended with a space, keep that space
        nonlocal i, text
        ws = 0
        while i + ws < len(text) and text[i + ws].isspace():
            ws += 1

        if text[i + ws - 1] == ' ':
            ws -= 1
        text = text[:i] + text[i+ws:]

    i = 0
    while i < len(text):
        if not text[i:i+len(CHOICE_START)] == CHOICE_START:
            i += 1
            continue

        # remove START
        text = text[:i] + text[i+len(CHOICE_START):]

        # remove whitespace
        consume_whitespace()

        cs = []
        c_start = i
        s_start = i
        while i < len(text):
            startswith = text[i:].startswith

            # recurse if START
            if startswith(CHOICE_START):
                consume_whitespace()
                consume_whitespace_pre()
                text = text[:i] + choose(text[i:]).strip()
            # add new choice
            elif startswith(CHOICE_SEP):
                consume_whitespace()
                consume_whitespace_pre()
                cs.append(text[c_start:i].strip())
                i += len(CHOICE_SEP)
                c_start = i
            # add last choice, choose
            elif startswith(CHOICE_END):
                consume_whitespace_pre()
                cs.append(text[c_start:i].strip())
                chosen = choice(cs)
                text = text[:s_start] + chosen + text[i+len(CHOICE_END):]
                i = s_start + len(chosen)
                consume_whitespace_post()
                break
            else:
                i += 1

    return text

