from pathlib import Path
from local.config import config
from local.rich.console import Console
from threading import Thread
from requests import head, Session, exceptions
from requests.adapters import HTTPAdapter

from local.rich.progress import (
    BarColumn,
    DownloadColumn,
    Progress,
    TextColumn,
    TimeElapsedColumn,
    TimeRemainingColumn,
    TransferSpeedColumn,
)

console = Console()

progress = Progress(
    TextColumn("[bold spring_green3]{task.fields[name]}", justify="right"),
    BarColumn(bar_width=30),
    "[progress.percentage]{task.percentage:>0.1f}%",
    "•",
    DownloadColumn(),
    "•",
    TransferSpeedColumn(),
    "•",
    TimeElapsedColumn(),
    "•",
    TimeRemainingColumn(),
)


class Download(object):
    def __init__(self):
        self.AAK = None
        self.getsize = 0
        self.chunk_size = 1024000
        self.num = int(config.THREAD) if config.THREAD else 64

    @staticmethod
    def _name(url):
        return Path(url).name

    @staticmethod
    def _size(url):
        return head(url, allow_redirects=True).headers['Content-Length']

    @staticmethod
    def _file(file_dir, name) -> str:
        return f'{file_dir}/{name}'

    def __update__(self, url, file_dir):
        return self._name(url), self._file(file_dir, self._name(url)), int(self._size(url))

    @staticmethod
    def __dict(start, end):
        return {'start': start, 'end': end}

    @staticmethod
    def _dict(value: dict):
        return value['start'], value['end']

    @staticmethod
    def _step(end, chunk) -> int:
        return end // chunk

    def block(self, start=0, end=0, chunk=0):
        rec = list(range(start, end, self._step(end, chunk)))
        rec[-1] = end + 1
        return rec

    def __block__(self, arr: list):
        return {
            i: self.__dict(start=arr[i], end=arr[i+1]-1)
            for i in range(len(arr)-1)
            }

    @staticmethod
    def _headers(start, end) -> dict:
        return {'range': f'bytes={start}-{end}'}

    @staticmethod
    def _write(file, start, chunk):
        with open(file, 'rb+') as f:
            f.seek(start)
            f.write(chunk)

    def __size(self, chunk):
        return chunk if chunk < self.chunk_size else self.chunk_size

    def _session(self, url, start, end):
        r = Session()
        retry = HTTPAdapter(max_retries=3)
        r.mount('http://', retry)
        r.mount('https://', retry)
        return r.get(url, headers=self._headers(start=start, end=end), stream=True, timeout=15)

    def download(self, url, file, start, end):
        for i in range(self._step(end=end - start, chunk=self.chunk_size) + 1):
            size = self.__size(chunk=start)
            try:
                for chunk in self._session(url, start, end).iter_content(size):
                    self._write(file, start, chunk)
                    start += len(chunk)
                    self.getsize += len(chunk)
            except exceptions.ConnectionError:
                pass

    def multithreading(self, url, file, num: int, block):
        for i in range(num):
            try:
                start, end = self._dict(block[i])
            except KeyError:
                start, end = self._dict(block)
            t = Thread(target=self.download, args=(url, file, start, end))
            t.start()

    def main(self, url, file_dir):
        console.clear()
        name, file, size = self.__update__(url, file_dir)
        block = self.__block__(self.block(end=size, chunk=self.num))
        if Path(file).is_file():
            old_size = int(Path(file).stat().st_size)
            if old_size != size:
                Path.unlink(Path(file))
            else:
                return file
        f = open(file, 'wb')
        f.close()
        self.multithreading(url, file, self.num, block)
        curr = 0
        console.print(f"正在下载固件 :\n  FILE_NAME: {name}\n  DOWNLOAD_DIR: {file_dir}\n",
                      style="medium_spring_green")
        with progress:
            task_id = progress.add_task("download", name='  ',  start=False)
            progress.update(task_id, total=size)
            while True:
                if self.AAK:
                    self.multithreading(url, file, 1, block=self.AAK)
                    self.AAK = None
                progress.start_task(task_id)
                down = self.getsize - curr
                progress.update(task_id, advance=down)
                curr += down
                if curr == size:
                    break
            return file

# https://hugeota.d.miui.com/22.2.22/miui_GAUGUINPRE_22.2.22_00696d7234_12.0.zip


download = Download().main
