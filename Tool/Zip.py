import tarfile
from zipfile import ZipFile
from Tool import Path, Console, sleep, shutil

console = Console()

class Find(object):
  def __init__(self, ZIP, Ziplist=None):
    self.zip = ZIP
    self.ziplist = Ziplist
  def file(self):
    try :
      zip = ZipFile(self.zip, 'r')
      for filename in zip.namelist():
        for i in self.ziplist:
          if filename == i:
            return str(self.zip.stem)
    except Exception as e :
      pass
          
class Zip(object):
  def __init__(self, Directory, Files):
    self.Directory = Directory
    self.Files = Files
  def Unzip(self):
    if Path(self.Directory).is_dir():
      shutil.rmtree(self.Directory)
    result = Path(self.Directory).mkdir(parents=True, exist_ok=True)
     
    if 'tar' == self.Files.rsplit('.', 2)[1] or self.Files.endswith('.tgz') or self.Files.endswith('./'):
      try :
        with tarfile.open(self.Files) as tar:
          tar.extract(self.Directory)
      except Exception as e :
        console.print(e, style="bold red"), sleep(0.5)
            
    elif self.Files.endswith('.zip'):
      try:
        with ZipFile(self.Files, mode="r") as zip:
          zip.extractall(self.Directory)
      except Exception as e:
        console.print(e, style="bold red"), sleep(0.5)

    else:
      console.print("文件格式不支持或者不是压缩文件", style="bold red")