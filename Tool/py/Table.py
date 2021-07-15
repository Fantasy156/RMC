"""Same as the table_movie.py but uses Live to update"""
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.table import Table
from rich import box

class Plug(object):
  def __init__(self, Variable):
    TABLE_DATA = [["[not italic]:page_facing_up:[/] 0", "返回上级", ]]
   
    n = 1
    for list in Variable:
      Row = ["[not italic]:printer:[/] %s" % (str(n)), list,]
      TABLE_DATA.append(Row)
      n += 1
      
    TABLE_DATA.append([" ", " ", " ", " ", ])  
    TABLE_DATA.append(["[not italic]:computer_disk:[/] 33-安装", "[not italic]:wastebasket:[/] 44-删除", "[not italic]:mobile_phone_off:[/] 88-退出", ])
    
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
      
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
        table.box = box.SIMPLE_HEAD
            
        table.add_column("序号", justify="center", no_wrap=True)
    
        table.add_column("名称", justify="left", no_wrap=True)
    
        table.title = (
                "[not italic]:right_arrow:[/] 固件列表 [not italic]:left_arrow:[/]"
            )
            
        for row in TABLE_DATA:
            table.add_row(*row)
    
        table.columns[0].style = "bright_cyan"
        table.columns[0].header_style = "bold cyan"
    
        table.columns[1].style = "bright_magenta"
        table.columns[1].header_style = "bold magenta"
        
        table.columns[2].style = "bright_red"
        table.columns[2].header_style = "bold red"

class FirmWare(object):
  def __init__(self, Variable):
    TABLE_DATA = [["[not italic]:page_facing_up:[/] 0", "返回上级", ]]
   
    n = 1
    for list in Variable:
      Row = ["[not italic]:printer:[/] %s" % (str(n)), list,]
      TABLE_DATA.append(Row)
      n += 1
    
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
      
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
        table.box = box.SIMPLE_HEAD
            
        table.add_column("序号", justify="center", no_wrap=True)
    
        table.add_column("名称", justify="left", no_wrap=True)
    
        table.title = (
                "[not italic]:right_arrow:[/] 固件列表 [not italic]:left_arrow:[/]"
            )
            
        for row in TABLE_DATA:
            table.add_row(*row)
    
        table.columns[0].style = "bright_cyan"
        table.columns[0].header_style = "bold cyan"
    
        table.columns[1].style = "bright_magenta"
        table.columns[1].header_style = "bold magenta"

class Delete_Project(object):
  def __init__(self, Variable):
    TABLE_DATA = [["[not italic]:page_facing_up:[/] 0", "返回上级", ]]
   
    n = 1
    for list in Variable:
      Row = ["[not italic]:printer:[/] %s" % (str(n)), list,]
      TABLE_DATA.append(Row)
      n += 1
    
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
      
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
        table.box = box.SIMPLE_HEAD
            
        table.add_column("序号", justify="center", no_wrap=True)
    
        table.add_column("名称", justify="left", no_wrap=True)
    
        table.title = (
                "[not italic]:right_arrow:[/] 项目列表 [not italic]:left_arrow:[/]"
            )
            
        for row in TABLE_DATA:
            table.add_row(*row)
    
        table.columns[0].style = "bright_cyan"
        table.columns[0].header_style = "bold cyan"
    
        table.columns[1].style = "bright_magenta"
        table.columns[1].header_style = "bold magenta"

class New_Project(object):
  def __init__(self, Variable):
    TABLE_DATA = [["[not italic]:page_facing_up:[/] 0", "新建工程", ]]
   
    n = 1
    for list in Variable:
      Row = ["[not italic]:printer:[/] %s" % (str(n)), list, ]
      TABLE_DATA.append(Row)
      n += 1
    
    TABLE_DATA.append([" ", " ", " ", " ", ])  
    TABLE_DATA.append(["[not italic]:computer_disk:[/] 33-解压", "[not italic]:wastebasket:[/] 44-删除", "[not italic]:down_arrow:[/] 66-下载", "[not italic]:mobile_phone_off:[/] 88-退出", ])
      
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
    
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
        table.box = box.SIMPLE_HEAD
            
        table.add_column("序号", justify="center", no_wrap=True)
    
        table.add_column("名称", justify="left", no_wrap=True)    
    
        table.title = (
                "[not italic]:right_arrow:[/] 项目列表 [not italic]:left_arrow:[/]"
            )
            
        for row in TABLE_DATA:
            table.add_row(*row)
        
        table.columns[2].style = "chartreuse3"
        table.columns[2].header_style = "bold chartreuse3"
        
        table.columns[3].style = "bright_red"
        table.columns[3].header_style = "bold red"
    
        table.columns[0].style = "bright_cyan"
        table.columns[0].header_style = "bold cyan"
    
        table.columns[1].style = "bright_magenta"
        table.columns[1].header_style = "bold magenta"
        
class Project(object):
  def __init__(self, Variable):
    TABLE_DATA = [
    [
        "[not italic]:printer:[/] 00> 选择 工程",
        "[not italic]:toolbox:[/] 01> 插件 sub",
    ],
    [
       "[not italic]:optical_disk:[/] 02> 分解 bin",
       "[not italic]:dvd:[/] 03> 打包 img",
    ],
    [
       "[not italic]:optical_disk:[/] 04> 分解 bro",
       "[not italic]:dvd:[/] 05> 打包 dat",
    ],
    [
       "[not italic]:optical_disk:[/] 06> 分解 dat",
       "[not italic]:dvd:[/] 07> 打包 bro",
    ],
    [
       "[not italic]:optical_disk:[/] 08> 分解 img",
       "[not italic]:floppy_disk:[/] 09> 打包 zip",
    ],
    [
    " ",
    " ",
    " ",
    " ",
    ],
    [
        "[not italic]:abacus:[/] 77> 其他",
        "[not italic]:mobile_phone_off:[/] 88-退出",
    ],
]
    console = Console()
    table = Table(show_footer=False)
    table_centered = Align.center(table)
    
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
        table.box = box.SIMPLE_HEAD
            
        table.add_column("[not italic]:optical_disk:[/] 解包", justify="center", no_wrap=True)
    
        table.add_column("[not italic]:dvd:[/] 打包", justify="center", no_wrap=True)
    
        table.title = (
                 "[not italic]:right_arrow:[/] 工程名称 > %s [not italic]:left_arrow:[/]" % (Variable)
                 )
    
        for row in TABLE_DATA:
            table.add_row(*row)
    
        table.columns[0].style = "bright_cyan"
        table.columns[0].header_style = "bold cyan"
    
        table.columns[1].style = "bright_magenta"
        table.columns[1].header_style = "bold magenta"
         
class Tablel(object):
  def __new__(self, Variable, Complete=None):
    if Complete == "New_project":
      New_Project(Variable)
    elif Complete == "Project":
      Project(Variable)
    elif Complete == "Delete_project":
      Delete_Project(Variable)
    elif Complete == "Firmware":
      FirmWare(Variable)
    elif Complete == "Plug":
      Plug(Variable)
    
    
    