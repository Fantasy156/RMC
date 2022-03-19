from functools import reduce
from time import strftime, localtime

from local.rich.console import Console

console = Console()


def prints(*args, style='turquoise2'):
    return console.print(f'{_data()}', *args, style=f'{style}', justify='left')


def _data():
    return strftime('%H%M%S', localtime())


def title(chara, style='turquoise2'):
    return f'[{style}] {chara} [/{style}]'


def inputs(args=None, style='turquoise2'):
    return console.input(f'[{style}] {args}[/]') if args else console.input()


def list_cutting(variable, number, num: int = 1, start=0):
    return _list_cut(_list_merge(_list_element_ist
                                 (variable, _list_generate(
                                   variable, number, start)))[0], num * 2)


def _list_element_ist(varia, data):
    return [[f'{idx}', item] for idx, item in zip(data, varia)]


def _list_cut(varia, num):
    return [varia[i:i + num] for i in range(0, len(varia), num)]


def _list_generate(varia, number, start):
    return number if number else [i for i in range(start, len(varia)+start)]


def _list_merge(varia):
    return varia if len(varia) == 1 else [reduce(lambda x, y: x.extend(y) or x, varia)]


def iseven(num, even):
    return num if num <= even else 0


def back_(chara):
    try:
        return int(chara)
    except ValueError:
        return None
