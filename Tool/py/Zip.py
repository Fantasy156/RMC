#!/usr/bin/env python3
# -*-coding:utf-8-*-
import zipfile, tarfile , zipfile, shutil
from pathlib import Path
from rich.console import Console

class Unzip(object):
  def __init__(self, PROJECT, FILES):
    console = Console()
    if Path(PROJECT).is_dir():
      shutil.rmtree(PROJECT)
    result = Path(PROJECT).mkdir(parents=True, exist_ok=True)
     
    if 'tar' == FILES.rsplit('.', 2)[1] or FILES.endswith('.tgz') or FILES.endswith('.tar'):
        try :
            tar = tarfile.open(FILES)  
            names = tar.getnames()   
            for name in names:  
                tar.extract(name, PROJECT)  
            tar.close()
        except Exception as e :
            print(e)
            
    elif FILES.endswith('.zip'):
        try :
            zip_file = zipfile.ZipFile(FILES)  
            for names in zip_file.namelist():  
                zip_file.extract(names, PROJECT)  
            zip_file.close()  
        except Exception as e :
            print(e)
            
    else:
      console.print("文件格式不支持或者不是压缩文件", style="bold red")