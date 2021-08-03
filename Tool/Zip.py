import tarfile
from zipfile import ZipFile
from Tool import Path, Console, sleep, shutil

class Find(object):
  def __new__(self, ZIP, Ziplist=None):
    try :
      z = ZipFile(ZIP, 'r')
      for filename in z.namelist():
        for i in Ziplist:
          if filename == i:
            return ZIP.stem
    except Exception as e :
      pass
          
class Unzip(object):
  def __init__(self, Directory, Files, Password=None):
    console = Console()
    if Path(Directory).is_dir():
      shutil.rmtree(Directory)
    result = Path(Directory).mkdir(parents=True, exist_ok=True)
     
    if 'tar' == Files.rsplit('.', 2)[1] or Files.endswith('.tgz') or Files.endswith('.tar'):
      try :
        tar = tarfile.open(Files)  
        names = tar.getnames()   
        for name in names:  
          tar.extract(name, Directory)  
        tar.close()
      except Exception as e :
        print(e), sleep(0.5)
            
    elif Files.endswith('.zip'):
      try:
        zip_file = ZipFile(Files)  
        for names in zip_file.namelist():  
          zip_file.extract(names, Directory)  
        zip_file.close()  
      except Exception as e:
        if 'password required for extraction' in str(e):
          print("加密文件请输入密码")
          Password = input()
          Unzip(Directory, Files, Password=None)
        else:
          print(e), sleep(0.5)

    else:
      console.print("文件格式不支持或者不是压缩文件", style="bold red")