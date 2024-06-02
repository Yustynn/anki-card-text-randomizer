from aqt.qt import *
import aqt
from random import choice

START = r'{r{'
END = r'}r}'
SEP = ':r:'

text = r"hey {r{I {r{believe:r:think}r}:r:there}r}"


def replace(text):
    i = 0
    while i < len(text):
        if not text[i:i+3] == START:
            i += 1
            continue

        text = text[:i] + text[i+3:]

        cs = []
        c_start = i
        s_start = i
        while i < len(text):
            seg = text[i:i+3]
            if seg == START:
                text = text[:i] + replace(text[i:])
            elif seg == SEP:
                cs.append(text[c_start:i].strip())
                i += 3
                c_start = i
            elif seg == END:
                cs.append(text[c_start:i].strip())
                chosen = choice(cs)
                text = text[:s_start] + chosen + text[i+3:]
                i = s_start + len(chosen)
                break
            else:
                i += 1

    return text

def on_card_will_show(text: str, card, kind):
    return replace(text)

aqt.gui_hooks.card_will_show.append(on_card_will_show)
