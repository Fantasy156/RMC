from getpass import getuser
from pathlib import Path

from local.config import config
from local.core import console, list_cutting, iseven
from local.rich import box
from local.rich.align import Align
from local.rich.live import Live
from local.rich.table import Table


def table(variable: list, header=None,
          styles: list = None, number: list = None, num=1, start=0):
    data = list_cutting(variable, number, num=num, start=start) if variable else [['没有刷机包']]
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
            for i in range(len(data[0])):
                table_data.columns[i].style = styles[idx]
                idx = iseven(num=idx + 1, even=len(styles) - 1)


def zip_dir(target):
    return f'/home/{getuser()}/{config.FILE_DIR}' if config.FILE_DIR else download_dir(target)


def download_dir(target):
    return f'/home/{getuser()}/Downloads' if target == 'PC' else None


def project_dir():
    return f'/home/{getuser()}/{config.PROJECT_DIR}' if config.PROJECT_DIR else Path.cwd()
