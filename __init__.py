from aqt.qt import *
import aqt
from random import choice

CHOICE_START = r'{r{'
CHOICE_END = r'}r}'
CHOICE_SEP = ':r:'


CHOICE_CONTEXT_KEY = 'Alt+Shift+c'
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

from anki.hooks import addHook

# cross out the currently selected text
def wrapChoose(editor):
    editor.web.eval("wrap('{r{ ', ' }r}');")

def addButtons(buttons, editor):
    editor._links['wrapChoose'] = wrapChoose
    return buttons + [editor.addButton(
        "iconpath",
        "wrapChoose",
        wrapChoose,
        tip=f"Wrap selection in a choose context ({CHOICE_CONTEXT_KEY})",
        keys=CHOICE_CONTEXT_KEY
    )]

addHook("setupEditorButtons", addButtons)
