#!/usr/bin/env python3
# -*-coding:utf-8-*-
import platform, subprocess
from itertools import cycle
from Tool import Zip, Path, Console, sleep, strftime, localtime
from Tool.Download import downloader
from Tool.Table import tabulation
from Tool.Utility import Except, Directory_Path, List, Mkdir, Delete
from Tool.Dcpdm import Task


try:
      
  def Bye():
    console.print("\n[i]感谢使用 [ R M C][/i]\n", style="bold bright_magenta", justify="center")
    exit()
    
  def Download():
    console.clear()
    console.print("\n下载固件\n", style="chartreuse3")
    url = input('    输入<压缩包>直链 >: ')
    downs = downloader(Directory=down, url=url)
    file = downs.main()
    Select(File=file)
    
    
  def In_Plug(PROJECT):
    console.clear()
    list = List(Path(down), "*.zip", Ziplist=['run.py', 'run.sh'])
    Style = ['bright_cyan', 'bright_magenta']
    Header_Style = ['bold cyan', 'bold magenta']
    Table = tabulation(list, Header='可安装插件列表', Other='返回上级', Style=Style, Header_Style=Header_Style)
    Table.Tablel()
    select = input('选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        pass
      elif int(len(list)) >= int(select):
        select = input('\033[1;31m[ ' + strftime('%H:%M:%S',localtime()) + ' ]         是否安装: ' + str(list[int(select) - 1]) + ' 插件 ? [1]: \033[0m')
        if Except(select).Select()[1] == True:
          if select == '1':
            Project = str(Path.cwd()) + '/Sub/' + str(list[int(select) - 1])
            File = down + "/" + str(list[int(select) - 1]) + ".zip"
            zip = Zip.Zip(Project, File)
            zip.Unzip()
            print('\033[1;31m[ ' + strftime('%H:%M:%S',localtime()) + ' ]         安装完成\033[0m')
      else:
        console.print("\n 没有次选项\n", style="bold red"), sleep(0.5)
    
    
  def Sub(PROJECT):
    console.clear()
    list = List(Path(str(Path.cwd()) + '/Sub'), "*", File=("run.*"), Filelist=['run.sh', 'run.py'])
    Options = [" 33-安装", " 44-删除", " 88-退出" ]
    Style = ['bright_cyan', 'bright_magenta', 'bright_red']
    Header_Style = ['bold cyan', 'bold magenta', 'bold red']
    Table = tabulation(list, Header='插件列表', Other='返回上级', Style=Style, Options=Options, Header_Style=Header_Style)
    Table.Tablel()
    select = input('选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        for _ in cycle((None,)): Project(PROJECT)
      elif select == '33':
        In_Plug(PROJECT)
      elif select == '44':
        path = str(Path.cwd()) + '/Sub'
        Delete_project(path, list)
      elif select == '88':
        Bye()
      elif int(len(list)) >= int(select):
        Plug = Directory_Path(str(Path.cwd()) + '/Sub' + "/" + str(list[int(select) - 1]), "*", Files=['run.sh', 'run.py']).list()[0]
        Path(Plug).chmod(0o777)
        subprocess.run([str(Plug) + ' ' + str(PROJECT)], shell=True)
      else:
        console.print("\n 没有此选项\n", style="bold red"), sleep(0.5)
    
  def Project(PROJECT):
    console.clear()
    Table = tabulation(PROJECT)
    Table.Tables()
    select = input('请输入序列号: ')
    if Except(select, Complete=True).Select()[1] == True:
      if select == '00':
        for _ in cycle((None,)): Home()
      elif select == '01':
        for _ in cycle((None,)): Sub(PROJECT)
      elif select == '02':
        pass
      elif select == '03':
        console.clear()
        Pack = Task(PROJECT=PROJECT, Task='Pack', name='br')
        Pack.main()
      elif select == '04':
        console.clear()
        Unpack = Task(PROJECT=PROJECT, Task='Unpack', name='br')
        Unpack.main()
      elif select == '05':
        console.clear()
        Pack = Task(PROJECT=PROJECT, Task='Pack', name='dat')
        Pack.main()
      elif select == '06':
        console.clear()
        Unpack = Task(PROJECT=PROJECT, Task='Unpack', name='new.dat')
        Unpack.main()
      elif select == '07':
        console.clear()
        Pack = Task(PROJECT=PROJECT, Task='Pack', name='img')
        Pack.main()
      elif select == '08':
        console.clear()
        Unpack = Task(PROJECT=PROJECT, Task='Unpack', name='img')
        Unpack.main()
      elif select == '09':
        pass
      elif select == '77':
        pass
      elif select == '88':
        Bye()
      else:
        console.print("\n 没有此选项\n", style="bold red"), sleep(0.5)
      
  def Delete_project(path, list=None):
    console.clear()
    if list:
      Style = ['bright_cyan', 'bright_magenta']
      Header_Style = ['bold cyan', 'bold magenta']
      Table = tabulation(list, Header='项目列表', Other='返回上级', Style=Style, Header_Style=Header_Style)
      Table.Tablel()
      select = input('请输入序号进行删除: ')
      if Except(select).Select()[1] == True:
        if select == '0':
          pass
        elif int(len(list)) >= int(select):
          Delete(str(path) + "/" + str(list[int(select) - 1]))
        else:
          console.print("\n 没有次选项\n", style="bold red"), sleep(0.5)

      
  def Select(File=None):
    console.clear()
    if not File:
      list = List(Path(down), "*", Filelist=['zip', 'tgz', 'tar'])
      Style = ['bright_cyan', 'bright_magenta']
      Header_Style = ['bold cyan', 'bold magenta']
      Table = tabulation(list, Header='可解压压缩包列表', Other='返回上级', Style=Style, Header_Style=Header_Style)
      Table.Tablel()
      select = input('> 选择: ')
      if Except(select).Select()[1] == True:
        if select == '0':
          pass
        elif int(len(list)) >= int(select):
          File = down + "/" + str(list[int(select) - 1])
        else:
          console.print("\n没有此选项\n", style="bold red"), sleep(0.5)
    if File:
      Name = str(Path.cwd()) + '/Error_' + str(Path(File).stem)
      console.clear()
      console.print('[bold red]解压固件 >[/bold red]\n\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), brea, Path(File).name), style="bold cyan")
      zip = Zip.Zip(Name, File)
      zip.Unzip()
      PROJECT = str(Path.cwd()) + '/' + str(Path(Name).name)
      Unpack = Task(PROJECT=PROJECT, Task='Unpack')
      Unpack.main()
      Project(PROJECT)


  def Home():
    console.clear()
    list = List(Path.cwd(), "Error_*")
    Options = [" 33-解压", " 44-删除", " 66-下载", " 88-退出" ]
    Style = ['bright_cyan', 'bright_magenta', 'chartreuse3', 'bright_red']
    Header_Style = ['bold cyan', 'bold magenta']
    Table = tabulation(list, Header='项目列表', Other='新建工程', Options=Options, Style=Style, Header_Style=Header_Style)
    Table.Tablel()
    select = input('> 选择: ')
    if Except(select).Select()[1] == True:
      if select == '0':
        console.clear()
        console.print("\n新建工程 >\n", style="turquoise2")
        files = input('      输入名称【不能有空格、特殊符号】: Error_')
        if files:
          PROJECT = str(Path.cwd()) + '/' + 'Error_' + files
          Mkdir(PROJECT)
      elif select == '33':
        Select()
      elif select == '44':
        Delete_project(Path.cwd(), list)
      elif select == '66':
        Download()
      elif select == '88':
        Bye()
      elif int(len(list)) >= int(select):
        PROJECT = str(Path.cwd()) + "/" + str(list[int(select) - 1])
        for _ in cycle((None,)): Project(PROJECT)
      else:
        console.print("\n 没有此选项\n", style="bold red"), sleep(0.5)


  console = Console()
  console.clear()
  console.print("\n正在初始化", style="bold chartreuse3")
  console.print("\n系统类型: ", platform.machine(), style="bold chartreuse3")
  console.print("\npython版本: ", platform.python_version(), style="bold chartreuse3")
  
  if Path('Tool').is_dir():
    LOCAL = Path.cwd()
    brea = '正在分解'
    
    if platform.machine() == 'x86_64':
      if Path('Tool/Make/linux').is_dir():        
        down = str(Path.cwd()) + '/Download'
        Binary = str(Path.cwd()) + '/Tool/Make/linux/'
        if not Path(down).is_dir():
          Path(down).mkdir(mode=0o777, exist_ok=True)
      else:
        console.clear()
        console.print("\n linux文件夹丢失 ...\n", style="bold red")
        
    elif platform.machine() == 'aarch64' or platform.machine() == 'armv8l' :
      if Path('Tool/Make/aarch64').is_dir():
        Binary = str(Path.cwd()) + '/Tool/Make/aarch64/'
        download = Directory_Path(Path('/'), '**/sdcard/download')
        down = download.str()
        if not Path(down).is_dir():
          Path(str(Path.cwd()) + '/Download').mkdir(mode=0o777, exist_ok=True)
          down = str(Path.cwd()) + '/Download'
      else:
        console.clear()
        console.print("\n aarch64文件夹丢失 ...\n", style="bold red")
        exit()
        
    else:
      console.clear()
      console.print("\n/ 不支持 <" + platform.machine() + "系统类型 ...\n", style="bold red")
      exit()
      
  else:
    console.clear()
    console.print("\n Tool文件夹丢失 ...\n", style="bold red")
    exit()    
  sleep(0.5)
  for _ in cycle((None,)): Home()


except KeyboardInterrupt:
  console.print("\n用户强制退出", style="bold red")
  Bye()