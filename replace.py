from random import choice

CHOICE_START = r'{r{'
CHOICE_END = r'}r}'
CHOICE_SEP = ':r:'

def replace(text):
    i = 0
    while i < len(text):
        if not text[i:i+len(CHOICE_START)] == CHOICE_START:
            i += 1
            continue

        # remove START
        text = text[:i] + text[i+len(CHOICE_START):]

        # remove whitespace
        ws = 0
        while text[i + ws].isspace():
            ws += 1
        text = text[:i] + text[i+ws:]

        cs = []
        c_start = i
        s_start = i
        while i < len(text):
            seg = text[i:i+len(CHOICE_START)]

            # recurse if START
            if seg == CHOICE_START:
                text = text[:i] + replace(text[i:]).strip()
            # add new choice
            elif seg == CHOICE_SEP:
                cs.append(text[c_start:i].strip())
                i += len(CHOICE_SEP)
                c_start = i
            # add last choice, choose
            elif seg == CHOICE_END:
                cs.append(text[c_start:i].strip())
                chosen = choice(cs)
                text = text[:s_start] + chosen + text[i+len(CHOICE_END):]
                i = s_start + len(chosen)
                break
            else:
                i += 1

    return text

