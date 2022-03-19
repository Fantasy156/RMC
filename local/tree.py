from pathlib import Path, PosixPath
from shutil import rmtree


def mkdir(directory):
    Path(directory).mkdir(parents=True) if not Path(directory).is_dir() else None


def find(files, directory):
    return [file.name for file in Path(directory).glob(files)]


def delete(directory):
    return rmtree(directory) if Path(directory).is_dir() else Path.unlink(Path(directory))
