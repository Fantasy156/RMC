#!/usr/bin/env python3
# -*-coding:utf-8-*-
import time, platform, subprocess, shutil, sys
from pathlib import Path, PurePath
from urllib.request import urlopen
from itertools import cycle
from rich.console import Console
sys.path.append('Tool/py/')
import Table, Zip
from Download import download

try:

  class Except(object):
    def __init__(self, Variable, Complete=None):
      self.Variable = Variable
      self.Complete = Complete
    def Select(self):
      try:
        float(self.Variable)
        if not self.Complete:
          if self.Variable != "0" and int(self.Variable) * 1 == 0:
            return console.print("\n输入错误\n", style="bold red"), time.sleep(0.5)
        return self.Variable, True
      except ValueError:
        return console.print("\n输入错误\n", style="bold red"), time.sleep(0.5)
        

  class List(object):
    def __new__(self, Directory, Search, Complete=None, Zip=None, Plug=None):
      list = []
      if (Zip):
        for res in Directory.glob(Search):
          NA = str(Path(res).suffixes)
          if 'zip' in NA or 'tgz' in NA or 'tar' in NA:
            all = list.append(str(res.name))
        list = sorted(set(list),key=list.index)
        return list
      else:
        for res in Directory.glob(Search):
          if Complete:
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
    console.print("\n[i]感谢使用 [ R M C][/i]\n", style="bold bright_magenta", justify="center")
    exit()
    
  def Download():
    console.clear()
    console.print("\n下载固件\n", style="chartreuse3")
    url = input('    输入<压缩包>直链 >: ')
    download(down, url)
    
  def Sub(PROJECT):
    subprocess.call('clear')
    list = List(Path(str(Path.cwd()) + '/Tool/Sub'), "*", Plug=True)
    Table.Tablel(list, Complete="Plug")
    select = input('选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        Project(PROJECT)
      elif select == '33':
        py = str(Path.cwd()) + '/Tool/py/Unpack/Sub.py'
        subprocess.run([ py + ' ' + str(down)], shell=True)
        Sub(PROJECT)
      elif select == '44':
      
        select = input('请输入序号进行删除: ')
        if Except(select).Select()[1] == True:
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
                    console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
                    Sub(PROJECT)
        else:
          console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
          Sub(PROJECT)
    
  def Project(PROJECT):
    console.clear()
    Table.Tablel(PROJECT, Complete="Project")
    select = input('请输入序列号: ')
    if Except(select, Complete=True).Select()[1] == True:
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
        console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
      
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
        console.print("\n 没有次选项\n", style="bold red"), time.sleep(0.5)
        
  def Select():
    subprocess.call('clear')
    list = List(Path(down), "*", Zip=True)
    Table.Tablel(list, Complete="Firmware")
    select = input('> 选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        for _ in cycle((None,)): Home()
      elif int(len(list)) >= int(select):
        File = down + "/" + str(list[int(select) - 1])
        Project = str(Path.cwd()) + '/Error_' + str(Path(File).stem)
        console.clear()
        console.print('[bold red]解压固件 >[/bold red]\n\n[ %s ] %10s %s' % (time.strftime('%H:%M:%S',time.localtime()), brea, Path(File).name), style="bold cyan")
        Zip.Unzip(Project, File)
      else:
        console.print("\n没有此选项\n", style="bold red"), time.sleep(0.5)
      
    
  def Home():
    console.clear()
    list = List(Path.cwd(), "Error_*")
    Table.Tablel(list, Complete="New_project")
    select = input('> 选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        console.clear()
        console.print("\n新建工程 >\n", style="turquoise2")
        files = input('      输入名称【不能有空格、特殊符号】: Error_')
        PROJECT = str(Path.cwd()) + '/' + 'Error_' + files
        console.print('\n%s' % (Mkdir(PROJECT)), style="bold red")
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
        console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
  console = Console()
  console.clear()
  console.print("\n正在初始化", style="bold chartreuse3")
  console.print("\n系统类型: ", platform.machine(), style="bold chartreuse3")
  console.print("\npython版本: ", platform.python_version(), style="bold chartreuse3")
  
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
        console.print("\n linux文件夹丢失 ...\n", style="bold red")
        
    elif platform.machine() == 'aarch64' or platform.machine() == 'armv8l' :
      if Path('Tool/aarch64').is_dir():
        Binary = str(Path.cwd()) + '/Tool/aarch64/'
        down = List(Path('/'), '**/sdcard/download', Complete=True)[0]
      else:
        console.clear()
        console.print("\n aarch64文件夹丢失 ...\n", style="bold red")
        exit()
        
    else:
      console.clear()
      console.print("\n 不支持 <" + platform.machine() + "系统类型 ...\n", style="bold red")
      exit()
      
  else:
    console.clear()
    console.print("\n Tool文件夹丢失 ...\n", style="bold red")
    exit()    
  time.sleep(0.5)
 
  for _ in cycle((None,)): Home()
except KeyboardInterrupt:
  console.print("\n用户强制退出", style="bold red")
  Bye()