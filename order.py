from random import shuffle

ORDER_START = r'[rorder]'
ORDER_END = r'[/rorder]'
ORDER_ITEM_START = r'[ritem]'
ORDER_ITEM_END = r'[/ritem]'

def order(text):

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



    i = 0
    while i < len(text):
        if not text[i:i+len(ORDER_START)] == ORDER_START:
            i += 1
            continue

        # remove ORDER_START
        text = text[:i] + text[i+len(ORDER_START):]

        # remove whitespace
        consume_whitespace()

        cs: tuple[int, str] = [] # [(start idx, raw string)]
        c_start = i
        offset = 0
        while i < len(text):
            startswith = text[i:].startswith

            # recurse if ORDER_START again
            if startswith(ORDER_START):
                consume_whitespace()
                text = text[:i] + order(text[i:]).strip()
            # start new element
            elif startswith(ORDER_ITEM_START):
                consume_whitespace()
                consume_whitespace_pre()
                c_start = i
                text = text[:i] + text[i+len(ORDER_ITEM_START):]

            # end new element
            elif startswith(ORDER_ITEM_END):
                consume_whitespace_pre()
                cs.append((c_start, text[c_start:i]))
                text = text[:i] + text[i+len(ORDER_ITEM_END):]
            # reorder
            elif startswith(ORDER_END):
                consume_whitespace_pre()
                text = text[:i] + text[i+len(ORDER_END):]
                order = [c[1].strip() for c in cs]
                shuffle(order)
                for el1, (idx, el2) in zip(order, cs):
                    l1 = len(el1)
                    l2 = len(el2)
                    text = text[:idx+offset] + el1 + text[idx+l2+offset:]
                    offset += l1 - l2
                break
            else:
                i += 1

    return text
