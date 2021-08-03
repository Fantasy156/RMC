#!/usr/bin/env python3
# -*-coding:utf-8-*-
import requests
from rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TaskID,
    TextColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

from Tool import Path, Console, sleep
from Tool.Utility import Mkdir

class download(object):
  def __new__(self, Directory, Url):
    console = Console()
    Mkdir(Directory)
   # if not Except(Url).Url()[0]:
      #return console.print(Except(Url).Url()[1], style="bold red"), Tool.time.sleep(1)    
    Url_size = int(requests.get(url=Url, stream=True).headers['Content-Length'])
    Url_file = Path(Url).name
    Res = Path(str(Directory) + '/' + Url_file)
    if Res.is_file():
      size = int(Res.stat().st_size)
      if Url_size != size:
        Path.unlink(Res)
      else:
        return console.print("文件已存在", style="bold red"), sleep(1)
        
    
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
      r = requests.get(Url, stream=True)
      task_id = progress.add_task("download", filename=Url_file, start=False)
      progress.update(task_id, total=Url_size)
      with open(str(Res), "wb") as dest_file:
        progress.start_task(task_id)
        for data in r.iter_content(chunk_size=1024):
          dest_file.write(data)
          progress.update(task_id, advance=len(data))
          