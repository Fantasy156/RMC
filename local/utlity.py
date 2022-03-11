from getpass import getuser

from local.config import config
from local.core import console, list_cutting, iseven
from local.rich import box
from local.rich.align import Align
from local.rich.live import Live
from local.rich.table import Table


def table(variable: list, header=None,
          styles: list = None, number: list = None, num=1):
    data, fre = list_cutting(variable, number, num=num)
    table_data = Table(show_footer=False)
    table_centered = Align.center(table_data)

    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        table_data.box = box.SIMPLE_HEAD
        if header:
            table_data.title = f'{header}'
        for row in data:
            table_data.add_row(*row)
        if styles:
            idx = 0
            for i in range(fre):
                table_data.columns[i].style = styles[idx]
                idx = iseven(num=idx + 1, even=len(styles) - 1)


def download_dir(target):
    match target:
        case 'PC':
            return f'/home/{getuser()}/{config.FILE_DIR}' if config.FILE_DIR else f'/home/{getuser()}/Downloads'

        case 'AARCH64':
            return f'/home/{getuser()}/{config.FILE_DIR}' if config.FILE_DIR else f'/home/{getuser()}/{config.FILE_DIR}'
