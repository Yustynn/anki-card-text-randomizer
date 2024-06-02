from aqt.qt import *
import aqt
from random import choice

CHOICE_START = r'{r{'
CHOICE_END = r'}r}'
CHOICE_SEP = ':r:'

def replace(text):
    i = 0
    while i < len(text):
        if not text[i:i+3] == CHOICE_START:
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
                text = text[:i] + replace(text[i:].strip())
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


def on_card_will_show(text: str, card, kind):
    return replace(text)

aqt.gui_hooks.card_will_show.append(on_card_will_show)

from aqt.utils import showInfo
from anki.hooks import addHook

# cross out the currently selected text
def wrapChoose(editor):
    editor.web.eval("wrap('{r{ ', ' }r}');")

def addMyButton(buttons, editor):
    editor._links['wrapChoose'] = wrapChoose
    return buttons + [editor._addButton(
        "iconname", # "/full/path/to/icon.png",
        "wrapChoose",
        "Wrap selection in a choose context")]

addHook("setupEditorButtons", addMyButton)