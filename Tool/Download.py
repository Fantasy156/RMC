from pathlib import Path
from threading import Thread
from requests import head, Session
from Tool.Utility import Mkdir
from Tool import Console, sleep, ConfigParser

from local.rich.progress import (
  BarColumn,
  DownloadColumn,
  Progress,
  TextColumn,
  TimeRemainingColumn,
  TransferSpeedColumn,
  )

console = Console()
cfp = ConfigParser()
cfp.read("Sub/config")

progress = Progress(
  TextColumn("[bold spring_green3]{task.fields[filename]}", justify="right"),
  BarColumn(bar_width=None),
  "[progress.percentage]{task.percentage:>0.1f}%",
  "•",
  DownloadColumn(),
  "•",
  TransferSpeedColumn(),
  "·",
  TimeRemainingColumn(),
  )


class downloader(object):
  def __init__(self, Directory, url):
    self.url = url
    self.num = cfp.get("download","Thread")
    self.name = Path(url).name
    self.Directory = Directory
    self.file = Directory + "/" + str(Path(url).name)
    self.getsize = 0
    self.curr = 0
    r = head(self.url, allow_redirects=True)
    self.size = int(r.headers['Content-Length'])
    self.chunk_size = 1024000
    self.one = True
    self.AAK = []
    self.s = Session()

  def down(self, start, end):
    headers = {'range': f'bytes={start}-{end}'}
    try:
      r = self.s.get(self.url, headers=headers, stream=True, timeout=15)
      with open(self.file, 'wb') as f:
        f.seek(start)
        for chunk in r.iter_content(self.chunk_size):
          f.write(chunk)
          f.flush()
          self.getsize += len(chunk)
          start += len(chunk)
    except Exception:
      return self.AAK.append((start, end))

  def Multithreading(self):
    if self.one:
      start = 0
      for i in range(self.num):
        end = int((i+1)/self.num*self.size)
        t = Thread(target=self.down, args=(start, end))
        t.start()
        start = end + 1
    elif self.AAK:
      for size in self.AAK:
        start = size[0] + 1
        end = size[1]
        t = Thread(target=self.down, args=(start, end))
        t.start()
        self.AAK.remove(size)

  def main(self):
    console.clear()
    Mkdir(self.Directory)
    Res = Path(self.file)
    if Res.is_file():
      size = int(Res.stat().st_size)
      if size != self.size:
        Path.unlink(Res)
      else:
        console.print("文件已存在", style="bold red"), sleep(1)
        return self.file
    self.Multithreading()
    self.one = False
    console.print("正在下载固件 :\n", style="medium_spring_green")
    with progress:
      task_id = progress.add_task("download", start=False)
      progress.update(task_id, total=self.size)
      while True:
        self.Multithreading()
        progress.start_task(task_id)
        down = self.getsize - self.curr
        progress.update(task_id, advance=down)
        self.curr += down
        if self.curr == self.size:
          break
      return self.file