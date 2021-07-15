#!/usr/bin/env python3
# -*-coding:utf-8-*-
import time, subprocess
from pathlib import Path, PurePath
from urllib.request import urlopen
from urllib import error
from functools import partial
from rich.console import Console

from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

class Info(object):
  def __new__(self, Variable):
    Format = Variable.info().get('Content-Type', -1).split('/')[0]
    if Format == 'application':
      return True, Variable.info().get('Content-Length', -1)
    else:
      return False, ''

class Except(object):
  def __init__(self, Variable):
    self.Variable = Variable
  def Directory(self):
    if not Path(self.Variable).is_dir():
      Path(self.Variable).mkdir(mode=0o777, exist_ok=True)
  def Url(self):
    try:
      r = urlopen(self.Variable)
      if Info(r)[0] == True:
        return True, Info(r)[1]
      else:
        return False, '链接内容不支持'
    except ValueError:
      return False, '未知 类型'
    except error.HTTPError as e:
      return False, e
    except error.URLError as e:
      return False, e

class download(object):
  def __new__(self, Directory, Url):
    console = Console()
    Except(Directory).Directory()
    if not Except(Url).Url()[0]:
      return console.print(Except(Url).Url()[1], style="bold red"), time.sleep(1)    
    Url_size = int(Except(Url).Url()[1])
    Url_file = Path(urlopen(Url).url).name
    Res = Path(str(Directory) + '/' + Url_file)
    if Res.is_file():
      size = int(Res.stat().st_size)
      if Url_size != size:
        Path.unlink(Res)
      else:
        return console.print("文件已存在", style="bold red"), time.sleep(1)
        
    
    progress = Progress(
    TextColumn("[bold spring_green3]{task.fields[filename]}", justify="right"),
    BarColumn(bar_width=None),
    "[progress.percentage]{task.percentage:>3.0f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "·",
    TimeRemainingColumn(),
    )
    
    console.clear()
    console.print("正在下载固件 :\n", style="medium_spring_green")
    with progress:
      response = urlopen(Url)
      task_id = progress.add_task("download", filename=Url_file, start=False)
      progress.update(task_id, total=Url_size)
      with open(str(Res), "wb") as dest_file:
        progress.start_task(task_id)
        for data in iter(partial(response.read, 1024), b""):
          dest_file.write(data)
          progress.update(task_id, advance=len(data))