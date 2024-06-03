from aqt.qt import *
from anki.hooks import addHook
import aqt
from .order import ORDER_ITEM_START, ORDER_ITEM_END, ORDER_START, ORDER_END
from .choose import CHOICE_START, CHOICE_END,  CHOICE_SEP
from .process import process
import os

ORDER_CONTEXT_KEY = 'Alt+Shift+o'
ORDER_ITEM_CONTEXT_KEY = 'Alt+Shift+i'

CHOICE_CONTEXT_KEY = 'Alt+Shift+c'
CHOICE_SEP_KEY = 'Alt+Shift+s'

def on_card_will_show(text: str, card, kind):
    return process(text)

def wrapChoose(editor):
    editor.web.eval(f"wrap('{CHOICE_START} ', ' {CHOICE_END}');")

def wrapOrder(editor):
    editor.web.eval(f"wrap('{ORDER_START} ', ' {ORDER_END}');")

def wrapOrderItem(editor):
    editor.web.eval(f"wrap('{ORDER_ITEM_START} ', ' {ORDER_ITEM_END}');")

def addChooseSeperator(editor):
    editor.web.eval(f"document.execCommand('insertText', false, ' {CHOICE_SEP} ');")

def addButtons(buttons, editor):
    editor._links['wrapChoose'] = wrapChoose
    buttons.append(editor.addButton(
        os.path.join(os.path.dirname(__file__), 'img', 'c.png' ),
        "wrapChoose",
        wrapChoose,
        tip=f"Wrap selection in a choose context ({CHOICE_CONTEXT_KEY})",
        keys=CHOICE_CONTEXT_KEY
    ))

    editor._links['addChooseSeperator'] = addChooseSeperator
    buttons.append(editor.addButton(
        os.path.join(os.path.dirname(__file__), 'img', 'cs.png' ),
        "addChooseSeperator",
        addChooseSeperator,
        tip=f"Add a choose seperator ({CHOICE_SEP_KEY})",
        keys=CHOICE_SEP_KEY
    ))

    editor._links['wrapOrder'] = wrapOrder
    buttons.append(editor.addButton(
        os.path.join(os.path.dirname(__file__), 'img', 'o.png' ),
        "wrapOrder",
        wrapOrder,
        tip=f"Wrap selection in an order context ({ORDER_CONTEXT_KEY})",
        keys=ORDER_CONTEXT_KEY
    ))

    editor._links['wrapOrderItem'] = wrapOrderItem
    buttons.append(editor.addButton(
        os.path.join(os.path.dirname(__file__), 'img', 'oi.png' ),
        "wrapOrderItem",
        wrapOrderItem,
        tip=f"Wrap selection in an order item ({ORDER_ITEM_CONTEXT_KEY})",
        keys=ORDER_ITEM_CONTEXT_KEY
    ))

    return buttons

aqt.gui_hooks.card_will_show.append(on_card_will_show)
addHook("setupEditorButtons", addButtons)