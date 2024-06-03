from aqt.qt import *
import aqt
from random import choice, shuffle

CHOICE_START = r'{r{'
CHOICE_END = r'}r}'
CHOICE_SEP = ':r:'

CHOICE_CONTEXT_KEY = 'Alt+Shift+c'

ORDER_START = r'{o{'
ORDER_END = r'}o}'
ORDER_ITEM_START = '{oi{'
ORDER_ITEM_END = '}oi}'

ORDER_CONTEXT_KEY = 'Alt+Shift+o'
ORDER_ITEM_CONTEXT_KEY = 'Alt+Shift+i'


def order(text):
    pass


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


def on_card_will_show(text: str, card, kind):
    return order(replace(text))

aqt.gui_hooks.card_will_show.append(on_card_will_show)

from anki.hooks import addHook

def wrapChoose(editor):
    editor.web.eval(f"wrap('{CHOICE_START} ', ' {CHOICE_END}');")

def wrapOrder(editor):
    editor.web.eval(f"wrap('{ORDER_START} ', ' {ORDER_END}');")

def wrapOrderItem(editor):
    editor.web.eval(f"wrap('{ORDER_ITEM_START} ', ' {ORDER_ITEM_END}');")

def addButtons(buttons, editor):
    editor._links['wrapChoose'] = wrapChoose
    buttons.append(editor.addButton(
        "iconpath",
        "wrapChoose",
        wrapChoose,
        tip=f"Wrap selection in a choose context ({CHOICE_CONTEXT_KEY})",
        keys=CHOICE_CONTEXT_KEY
    ))

    editor._links['wrapOrder'] = wrapOrder
    buttons.append(editor.addButton(
        "iconpath",
        "wrapOrder",
        wrapOrder,
        tip=f"Wrap selection in an order context ({ORDER_CONTEXT_KEY})",
        keys=ORDER_CONTEXT_KEY
    ))

    editor._links['wrapOrderItem'] = wrapOrderItem
    buttons.append(editor.addButton(
        "iconpath",
        "wrapOrderItem",
        wrapOrderItem,
        tip=f"Wrap selection in an order context ({ORDER_ITEM_CONTEXT_KEY})",
        keys=ORDER_ITEM_CONTEXT_KEY
    ))



    return buttons

addHook("setupEditorButtons", addButtons)
