from .order import order
from .choose import choose

def process(text):
    return order(choose(text))

if __name__ == '__main__':
    """ hacky tests """
    text = """
    {c{
    LLVM stands for {{c1::Low Level Virtual Machine}} 
    {c{ despite being :c: although it's  :c: which is ironic because it's }c}
    a {{c2::compilation infrastructure}}
    :c:
    {c{
    Despite being more of  :c: 
    While it's  :c: 
    }c}
    a {{c2::compilation infrastructure}}, LLVM stands for {{c1::Low Level Virtual Machine}}
    }c}
    """

    for _ in range(50):
        t = process(text)
        if "although" in t:
            print(t)