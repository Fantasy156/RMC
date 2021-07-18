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
    def __new__(self, Directory, Search, Complete=None, Archive=None, ZIp=None, Ziplist=None, Plug=None, File=None, Filelist=None, Files=None):
      list = []
      if Archive:
        for res in Directory.glob(Search):
          NA = str(Path(res).suffixes)
          for i in Filelist:
            if i in NA:
              all = list.append(str(res.name))
        list = sorted(set(list),key=list.index)
        return list
      elif ZIp:
        for ZIP in Directory.glob(Search):
          if Zip.Find(ZIP, Ziplist) != None:
            all = list.append(str(Zip.Find(ZIP, Ziplist)))
        list = sorted(set(list),key=list.index)
        return list
      elif Files:
        for res in Directory.glob(Search):
          for i in Filelist:
            if res.name == i:
              return res
      else:
        for res in Directory.glob(Search):
          if Complete:
            all = list.append(str(res))
          else:
            if Plug:
              for ress in Path(res).glob(File):
                for i in Filelist:
                  if ress.name == i:
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
    
  def In_Plug(PROJECT):
    console.clear()
    list = List(Path(down), "*.zip", ZIp=True, Ziplist=['run.py', 'run.sh'])
    Style = ['bright_cyan', 'bright_magenta']
    Header_Style = ['bold cyan', 'bold magenta']
    Table.Tablel(list, Header='可安装插件列表', Other='返回上级', Style=Style, Options=Options, Header_Style=Header_Style)
    select = input('选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        for _ in cycle((None,)): Sub(PROJECT)
      elif int(len(list)) >= int(select):
        select = input('\033[1;31m[ ' + time.strftime('%H:%M:%S',time.localtime()) + ' ]         是否安装: ' + str(list[int(select) - 1]) + ' 插件 ? [1]: \033[0m')
        if Except(select).Select()[1] == True:
          if select == '1':
            Project = str(Path.cwd()) + '/Tool/Sub/' + str(list[int(select) - 1])
            File = down + "/" + str(list[int(select) - 1]) + ".zip"
            Zip.Unzip(Project, File)
            print('\033[1;31m[ ' + time.strftime('%H:%M:%S',time.localtime()) + ' ]         安装完成\033[0m')
      else:
        console.print("\n 没有次选项\n", style="bold red"), time.sleep(0.5)
    
    
  def Sub(PROJECT):
    console.clear()
    list = List(Path(str(Path.cwd()) + '/Tool/Sub'), "*", Plug=True, File="run.*", Filelist=['run.sh', 'run.py'])
    Options = [" 33-安装", " 44-删除", " 88-退出" ]
    Style = ['bright_cyan', 'bright_magenta', 'bright_red']
    Header_Style = ['bold cyan', 'bold magenta', 'bold red']
    Table.Tablel(list, Header='插件列表', Other='返回上级', Style=Style, Options=Options, Header_Style=Header_Style)
    select = input('选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        for _ in cycle((None,)): Project(PROJECT)
      elif select == '33':
        for _ in cycle((None,)): In_Plug(PROJECT)
      elif select == '44':
        console.clear()
        Style = ['bright_cyan', 'bright_magenta']
        Header_Style = ['bold cyan', 'bold magenta']
        Table.Tablel(list, Header='插件列表', Style=Style, Header_Style=Header_Style)
        select = input('请输入序号进行删除: ')
        if Except(select).Select()[1] == True:
          if int(len(list)) >= int(select):
            Delete(str(Path.cwd()) + '/Tool/Sub' + "/" + str(list[int(select) - 1]))
          else:
            console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
      elif select == '88':
        Bye()
      elif int(len(list)) >= int(select):
        Plug = List(Path(str(Path.cwd()) + '/Tool/Sub' + "/" + str(list[int(select) - 1])), "*", Filelist=['run.sh', 'run.py'], Files=True)
        Path(Plug).chmod(0o777)
        subprocess.run([str(Plug) + ' ' + str(PROJECT)], shell=True)
      else:
        console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
    
  def Project(PROJECT):
    console.clear()
    Table.Project(PROJECT)
    select = input('请输入序列号: ')
    if Except(select, Complete=True).Select()[1] == True:
      if select == '00':
        for _ in cycle((None,)): Home()
      elif select == '01':
        for _ in cycle((None,)): Sub(PROJECT)
      elif select == '02':
        pass
        Unpack(PROJECT, select)
      elif select == '03':
        console.clear()
        pass
      elif select == '04':
        console.clear()
        pass
      elif select == '05':
        pass
      elif select == '06':
        pass
      elif select == '07':
        pass
      elif select == '08':
        pass
      elif select == '09':
        pass
      elif select == '77':
        pass
      elif select == '88':
        Bye()
      else:
        console.print("\n 没有此选项\n", style="bold red"), time.sleep(0.5)
      
  def Delete_project():
    console.clear()
    list = List(Path.cwd(), "Error_*")
    Style = ['bright_cyan', 'bright_magenta']
    Header_Style = ['bold cyan', 'bold magenta']
    Table.Tablel(list, Header='项目列表', Other='返回上级', Style=Style, Header_Style=Header_Style)
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
    list = List(Path(down), "*", Archive=True, Filelist=['zip', 'tgz', 'tar'])
    Style = ['bright_cyan', 'bright_magenta']
    Header_Style = ['bold cyan', 'bold magenta']
    Table.Tablel(list, Header='可解压压缩包列表', Other='返回上级', Style=Style, Header_Style=Header_Style)
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
    Options = [" 33-解压", " 44-删除", " 66-下载", " 88-退出" ]
    Style = ['bright_cyan', 'bright_magenta', 'chartreuse3', 'bright_red']
    Header_Style = ['bold cyan', 'bold magenta']
    Table.Tablel(list, Header='项目列表', Other='新建工程', Options=Options, Style=Style, Header_Style=Header_Style)
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
        if not Path(down).is_dir():
          Path(str(Path.cwd()) + '/Download').mkdir(mode=0o777, exist_ok=True)
          down = str(Path.cwd()) + '/Download'
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