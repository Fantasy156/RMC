#!/usr/bin/env python3
# -*-coding:utf-8-*-
import time, platform, subprocess, shutil, sys
from pathlib import Path, PurePath
from urllib.request import urlopen
from itertools import cycle
from rich.console import Console
sys.path.append('Tool/py/')
import Table
from Download import download

try:

  class Except(object):
    def __init__(self, Variable):
      self.Variable = Variable
    def Select(self):
      try:
        float(self.Variable)
        return self.Variable, True
      except ValueError:
        return print('输入错误'), time.sleep(0.5)
        

  class List(object):
    def __new__(self, Directory, Search, Complete=None, Zip=None, Plug=None):
      list = []
      if (Zip):
        for res in Directory.glob(Search):
          NA = str(Path(res).suffixes)
          if 'zip' in NA or 'tgz' in NA or 'tar' in NA or 'rar' in NA:
            all = list.append(str(res.name))
        list = sorted(set(list),key=list.index)
        return list
      else:
        for res in Directory.glob(Search):
          if (Complete):
            all = list.append(str(res))
          else:
            if (Plug):
              for ress in Path(res).glob('run.*'):
                if ress.name == 'run.sh' or ress.name == 'run.py':
                  all = list.append(str(res.name))
            else:
              all = list.append(str(res.name))
        list = sorted(set(list),key=list.index)
        return list
  
  class Mkdir(object):
    def __new__(self, Directory):
      if  not Path(Directory).is_dir():
        Path(Directory).mkdir(mode=0o777, exist_ok=True)
        return ''
      else:
        return '创建失败'
        
  class Delete(object):
    def __new__(self, Directory):
      shutil.rmtree(Directory)
      
  def Bye():
    print('\033[1;35m> 感谢使用 [ R.M.C ] \033[0m\n'), time.sleep(0.5)
    exit()
    
  def Download():
    console.clear()
    print('\033[1;31m> 下载固件: \033[0m' )
    url = input('    输入<压缩包>直链 >: ')
    download(down, url)
    
  def Sub(PROJECT):
    subprocess.call('clear')
    list = List(Path(str(Path.cwd()) + '/Tool/Sub'), "*", Plug=True)
    Table.Tablel(list, Complete="Plug")
    select = input('选择: ')
    try:
      float(select)
    except ValueError:
      print('输入错误'), time.sleep(0.1)      
      Sub(PROJECT)
    if select == '0':
      Project(PROJECT)
    elif select == '33':
      py = str(Path.cwd()) + '/Tool/py/Unpack/Sub.py'
      subprocess.run([ py + ' ' + str(down)], shell=True)
      Sub(PROJECT)
    elif select == '44':
    
      select = input('请输入序号进行删除: ')
      try:
        float(select)
      except ValueError:
        print('输入错误'), time.sleep(0.1)      
        Sub(PROJECT)
      if int(qt) >= int(select):
        qt = 1
        for res in Path(str(Path.cwd()) + '/Tool/Sub').glob('*'):
          for ress in Path(res).glob('run.*'):
            if ress.name == 'run.sh' or ress.name == 'run.py':
              if select == str(qt):
                shutil.rmtree(res)
                Sub(PROJECT)
              elif int(select) > int(qt):
                qt = int(qt) + 1
              else:
                print('没有此选项'), time.sleep(0.1)
                Sub(PROJECT)
      else:
        print('没有此选项'), time.sleep(0.1)
        Sub(PROJECT)
    
  def Project(PROJECT):
    console.clear()
    Table.Tablel(PROJECT, Complete="Project")
    select = input('请输入序列号: ')
    try:
      float(select)
    except ValueError:
      print('输入错误'), time.sleep(0.5)
    if select == '00':
      for _ in cycle((None,)): Home()
    elif select == '01':
      for _ in cycle((None,)): Sub(PROJECT)
    elif select == '02':
      console.clear()
      Unpack(PROJECT, select)
    elif select == '03':
      console.clear()
      Unpack(PROJECT, select)
    elif select == '04':
      console.clear()
      Unpack(PROJECT, select)
    elif select == '05':
      Sub(PROJECT)
    elif select == '06':
      Pack(PROJECT, select)
    elif select == '07':
      Pack(PROJECT, select)
    elif select == '08':
      Pack(PROJECT, select)
    elif select == '09':
      Zip(PROJECT)
    elif select == '77':
      Other(PROJECT)
    elif select == '88':
      Bye()
    else:
      print('没有此选项'), time.sleep(0.5)
      
  def Delete_project():
    console.clear()
    list = List(Path.cwd(), "Error_*")
    Table.Tablel(list, Complete="Delete_project")
    select = input('请输入序号进行删除: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        for _ in cycle((None,)): Home()
      elif int(len(list)) >= int(select):
        Delete(str(Path.cwd()) + "/" + str(list[int(select) - 1]))
      else:
        print('没有此选项'), time.sleep(0.5)
        
  def Select():
    subprocess.call('clear')
    list = List(Path(down), "*", Zip=True)
    Table.Tablel(list, Complete="Firmware")
    select = input('> 选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        for _ in cycle((None,)): Home()
      elif int(len(list)) >= int(select):
        PROJECT = str(Path.cwd()) + "/" + str(list[int(select) - 1])
        Unzip(PROJECT)
      else:
        print('没有此选项'), time.sleep(0.5)
      
    
  def Home():
    console.clear()
    list = List(Path.cwd(), "Error_*")
    Table.Tablel(list, Complete="New_project")
    select = input('> 选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        console.clear()
        print('\033[1;31m> 新建工程\033[0m\n')
        files = input('      输入名称【不能有空格、特殊符号】: Error_')
        PROJECT = str(Path.cwd()) + '/' + 'Error_' + files
        print('\033[1;31m\n%s>\033[0m\n' % (Mkdir(PROJECT))), time.sleep(0.5)
      elif select == '33':
        for _ in cycle((None,)): Select()
      elif select == '44':
        for _ in cycle((None,)): Delete_project()        
      elif select == '66':
        Download()
      elif select == '88':
        Bye()
      elif int(len(list)) >= int(select):
        PROJECT = str(Path.cwd()) + "/" + str(list[int(select) - 1])
        for _ in cycle((None,)): Project(PROJECT)
      else:
        print('没有此选项'), time.sleep(0.5)
  console = Console()
  console.clear()
  print('\033[1;32m正在初始化 ...\033[0m\n')
  print('\033[1;32m系统类型: ', platform.machine(), '\033[0m\n')
  print('\033[1;32mpython版本: ', platform.python_version(), '\033[0m')
  
  if Path('Tool').is_dir():
    LOCAL = Path.cwd()
    brea = '正在分解'
    
    if platform.machine() == 'x86_64':
      if Path('Tool/linux').is_dir():        
        down = str(Path.cwd()) + '/Download'
        Binary = str(Path.cwd()) + '/Tool/linux/'
        if not Path(down).is_dir():
          Path(down).mkdir(mode=0o777, exist_ok=True)
      else:
        console.clear()
        print('\033[1;33m\n linux文件夹丢失 ...\033[0m\n')
        
    elif platform.machine() == 'aarch64' or platform.machine() == 'armv8l' :
      if Path('Tool/aarch64').is_dir():
        Binary = str(Path.cwd()) + '/Tool/aarch64/'
        down = List(Path('/'), '**/sdcard/download', Complete=True)[0]
      else:
        console.clear()
        print('\033[1;31m\n aarch64文件夹丢失 ...\033[0m\n')
        exit()
        
    else:
      console.clear()
      print('\033[1;31m\n 不支持 <' + platform.machine() + '> 系统类型 ...\033[0m\n')
      exit()
      
  else:
    console.clear()
    print('\033[1;31m\n Tool文件夹丢失 ...\033[0m\n')
    exit()    
  time.sleep(0.5)
 
  for _ in cycle((None,)): Home()
except KeyboardInterrupt:
  print('\n\033[1;31m> 用户强制退出\033[0m\n\n')
  Bye()