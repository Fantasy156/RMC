from pathlib import Path
from local.config import config
from local.rich.console import Console
from threading import Thread, Lock
from requests import head, Session, exceptions
import gc

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
        self.chunk_size = 1024000
        self.quick_ = []
        self.lock = Lock()
        self.num = int(config.THREAD) if config.THREAD else 1

    @staticmethod
    def _size(url):
        return head(url, allow_redirects=True).headers['Content-Length']

    def __update__(self, url, file_dir):
        return Path(url).name, f'{file_dir}/{Path(url).name}', int(self._size(url))

    @staticmethod
    def __dict(start, end, tag):
        return {'start': start, 'end': end, 'tag': tag}

    @staticmethod
    def dict(value, tag):
        return value[tag]

    @staticmethod
    def revise_quick(quick, key, value):
        quick[key] = value

    @staticmethod
    def quick_size(size, num):
        return size // num

    def quick_start(self, i, end):
        return i * self.quick_size(end, self.num)

    def quick_end(self, i, end):
        return end if (i + 1) == self.num \
            else (i + 1) * self.quick_size(end, self.num) - 1

    def quick(self, end):
        return {
            i: self.__dict(start=self.quick_start(i, end),
                           end=self.quick_end(i, end),
                           tag=True)
            for i in range(self.num)
        }

    def quick_list(self):
        return [i for i in range(self.num)
                if self.dict(self.quick_[i], 'tag') and
                not self.judge(self.dict(self.quick_[i], 'start'),
                               self.dict(self.quick_[i], 'end'))]

    def update_progress(self, initial, quick):
        return sum(self.get_quick(quick, 'start')) - initial, sum(self.get_quick(quick, 'start'))

    def get_quick(self, quick, tag):
        return [self.dict(quick[i], tag) for i in range(self.num)]

    @staticmethod
    def _headers(start, end) -> dict:
        return {'range': f'bytes={start}-{end}'}

    def thread_list(self, url, file, quick, quick_list=()):
        return [
            Thread(target=self.download,
                   args=(i, url, file, self.dict(quick[i], 'start'), self.dict(quick[i], 'end')))
            for i in quick_list
        ]

    @staticmethod
    def judge(start, end):
        return False if start < end else True

    @staticmethod
    def path(file):
        return Path(file).stat().st_size if Path(file).is_file() else False

    def verify_file(self, file, size):
        return True if self.path(file) == size else False

    def verify(self):
        for i in range(self.num):
            if not self.judge(self.dict(self.quick_[i], 'start'), self.dict(self.quick_[i], 'end')):
                return False
        return True

    @staticmethod
    def thread(thread_list):
        for t in thread_list:
            t.start()

    def download(self, i, url, file, start, end):
        self.revise_quick(self.quick_[i], key='tag', value=False)
        headers = {'range': f'bytes={start}-{end}'}
        try:
            r = Session().get(url, headers=headers, stream=True)
            for chunk in r.iter_content(self.chunk_size):
                self.lock.acquire()
                file.seek(start)
                file.write(chunk)
                start += len(chunk)
                self.revise_quick(self.quick_[i], key='start', value=start)
                self.lock.release()
        except exceptions.ProxyError:
            pass
        if start < end:
            self.revise_quick(self.quick_[i], key='tag', value=True)

    def main(self, url, file_dir):
        console.clear()
        name, file, size = self.__update__(url, file_dir)
        if self.verify_file(file, size):
            return file
        self.quick_ = self.quick(size)
        initial = sum(self.get_quick(self.quick_, 'start'))
        with open(file, 'wb') as f:
            console.print(f"正在下载固件 :\n  FILE_NAME: {name}\n  DOWNLOAD_DIR: {file_dir}\n",
                          style="medium_spring_green")
            with progress:
                task_id = progress.add_task("download", name=' ', start=False)
                progress.start_task(task_id)
                progress.update(task_id, total=size)
                while True:
                    thread_list = self.thread_list(url, f, self.quick_, self.quick_list())
                    self.thread(thread_list)
                    curr, initial = self.update_progress(initial, self.quick_)
                    console.print('', end='\r')
                    progress.update(task_id, advance=curr)
                    if self.verify():
                        break
        return file if self.verify_file(file, size) else False


# https://hugeota.d.miui.com/22.2.22/miui_GAUGUINPRE_22.2.22_00696d7234_12.0.zip


download = Download().main
