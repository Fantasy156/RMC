from getpass import getuser
from pathlib import Path
from local.config import config
from local.dwonload import download


def run(target):
    file_dir = download_dir(target)
    url = input('')
    download(url, file_dir)

def download_dir(target):
    file_dir = ''
    if target == 'PC':
        directory = f'/home/{getuser()}/下载'
        file_dir = directory if Path(directory).is_dir() else f'/home/{getuser()}/download'
        if config.FILE_DIR:
            file_dir = f'/home/{getuser()}/{config.FILE_DIR}'
            Path(file_dir).mkdir()

    elif target == 'AARCH64':
        pass

    return file_dir
