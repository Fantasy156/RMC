#!/usr/bin/env python3
# -*-coding:utf-8-*-
import zipfile, tarfile , zipfile, shutil
from pathlib import Path
from rich.console import Console

class Find(object):
  def __new__(self, ZIP, Ziplist=None):
    try :
      z = zipfile.ZipFile(ZIP, 'r')
      for filename in z.namelist():
        for i in Ziplist:
          if filename == i:
            return ZIP.stem
    except Exception as e :
      pass
          
class Unzip(object):
  def __init__(self, Directory, Files):
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
            print(e)
            
    elif Files.endswith('.zip'):
        try :
            zip_file = zipfile.ZipFile(Files)  
            for names in zip_file.namelist():  
                zip_file.extract(names, Directory)  
            zip_file.close()  
        except Exception as e :
            print(e)
            
    else:
      console.print("文件格式不支持或者不是压缩文件", style="bold red")