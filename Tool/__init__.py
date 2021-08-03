import shutil
from pathlib import Path
from functools import partial
from time import sleep, localtime, strftime
from rich.console import Console
from Tool.Unpack import Decompress
from Tool.Utility import Directory_Path

class Unpack(object):
  def __new__(self, **kwargs):
    files = Directory_Path(Path(kwargs['PROJECT']), '*.' + kwargs['name'])
    for file in files:
      Decompress(file, Unpack=kwargs['name'])