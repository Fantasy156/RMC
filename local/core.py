from functools import reduce
from time import strftime, localtime

from local.rich.console import Console

console = Console()


def prints(*args, style='bold cyan'):
    date = strftime('%H%M%S', localtime())
    console.print(f'{date}', *args, style=style, justify='left')


def inputs(args, style='bold cyan'):
    console.input(f'[{style}] {args}[/]')


def list_cutting(variable, number, num: int = 1):
    return list_cut(list_merge(list_element_ist
                    (variable, list_generate(
                     variable, number)))[0], num * 2), \
           num * 2


def list_element_ist(varia, data):
    return [[f'{idx}', item] for idx, item in zip(data, varia)]


def list_cut(varia, num):
    return [varia[i:i + num] for i in range(0, len(varia), num)]


def list_generate(varia, number):
    return number if number else [i for i in range(len(varia))]


def list_merge(varia):
    return varia if len(varia) == 1 else [reduce(lambda x, y: x.extend(y) or x, varia)]


def iseven(num, even):
    nums = 0
    return num if num <= even else nums
