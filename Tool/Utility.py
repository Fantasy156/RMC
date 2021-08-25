import re
from Tool import Path, Console, sleep, shutil, Zip
from multiprocessing import Process

console = Console()

class Except(object):
  def __init__(self, Variable, Complete=None):
    self.Variable = Variable
    self.Complete = Complete

  def Select(self):
    try:
      float(self.Variable)
      if not self.Complete:
        if self.Variable != "0" and re.search('^0[0-9]+$', self.Variable):
          return console.print("\n输入错误\n", style="bold red"), sleep(0.5)
      return self.Variable, True
    except ValueError:
      return console.print("\n输入错误\n", style="bold red"), sleep(0.5)
        
class Directory_Path(object):
  def __init__(self, Directory, Search, Files=None):
    self.Directory = Path(Directory)
    self.Files = Files
    self.Search = Search

  def str(self):
    for res in self.Directory.glob(self.Search): 
      return str(res)

  def list(self):
    list = []
    for res in self.Directory.glob(self.Search):
      if self.Files:
        for i in self.Files:
          if res.name == i:
            list.append(str(res))
      else:
        list.append(str(res))
    list = sorted(set(list),key=list.index)
    return list

class List(object):
  def __new__(self, Directory, Search, File=None, Filelist=None, Ziplist=None):
    list = []
    for res in Directory.glob(Search):
      if Filelist:
        if File:
          for ress in Path(res).glob(File):
            for i in Filelist:
              if ress.name == i:
                all = list.append(str(res.name))
        else:
          for i in Filelist:
            try:
              if i == str(Path(res).name).rsplit('.', 1)[1]:
                list.append(str(res.name))
              elif 'tar' == str(Path(res).name).rsplit('.', 2)[1]:
                list.append(str(res.name))
            except IndexError:
              pass
      elif Ziplist:
        if Zip.Find(res, Ziplist).file() != None:
          list.append(Zip.Find(res, Ziplist).file())
      else:
        list.append(str(res.name))
    list = sorted(set(list),key=list.index)
    return list
  
class Mkdir(object):
  def __init__(self, Directory, mode=None):
    if  not Path(Directory).is_dir():
      if mode:
        self.mode = mode
      else:
        self.mode = 0o777 
      Path(Directory).mkdir(mode=0o777)

class Delete(object):
  def __init__(self, src=None):
    if type(src) is list:
      for path in src:
        if Path(path).is_dir():
          shutil.rmtree(path)
        elif Path(path).is_file():
          Path.unlink(Path(path))
    else:
      if Path(src).is_dir():
        shutil.rmtree(str(src))
      elif Path(src).is_file():
        Path.unlink(Path(src))