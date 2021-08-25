"""Same as the table_movie.py but uses Live to update"""
from rich.align import Align
from rich.live import Live
from rich.table import Table
from rich import box

from Tool import Console

console = Console()

class tabulation(object):
  def __init__(self, Variable, Header=None, Other=None, Options=None, Style=None, Header_Style=None):
    self.Variable = Variable
    self.Header = Header
    self.Other = Other
    self.Options = Options
    self.Style = Style
    self.Header_Style = Header_Style
  def Tablel(self):
    if self.Other:
      TABLE_DATA = [[" 0", "%s" % (self.Other), ]]
   
    n = 1
    for list in self.Variable:
      Row = [" %s" % (str(n)), list, ]
      TABLE_DATA.append([" ",])
      TABLE_DATA.append(Row)
      n += 1
    
    TABLE_DATA.append([" ",])
    
    if self.Options:
      TABLE_DATA.append(self.Options)
      
    table = Table(show_footer=False)
    table_centered = Align.center(table)
    
    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
      table.box = box.SIMPLE_HEAD
            
      table.add_column("序号", justify="center", no_wrap=True)
    
      table.add_column("名称", justify="left", no_wrap=True)    
    
      table.title = (" %s " % (self.Header))
            
      for row in TABLE_DATA:
        table.add_row(*row)
        
      if self.Style:
        n = 0
        for style in self.Style:
          table.columns[n].style = style
          n += 1
            

      if self.Header_Style:
        n = 0
        for style in self.Header_Style:
          table.columns[n].header_style = style
          n += 1
        
  def Tables(self):
    TABLE_DATA = [
    [
        " 00> 选择 工程",
        " 01> 插件 sub",
    ],
    [
       " 02> 分解 bin",
       " 03> 打包 bro",
    ],
    [
       " 04> 分解 bro",
       " 05> 打包 dat",
    ],
    [
       " 06> 分解 dat",
       " 07> 打包 img",
    ],
    [
       " 08> 分解 img",
       " 09> 打包 zip",
    ],
    [
    " ",
    " ",
    ],
    [
        " 77> 其他",
        " 88-退出",
    ],
]

    table = Table(show_footer=False)
    table_centered = Align.center(table)

    with Live(table_centered, console=console, screen=False, refresh_per_second=20):
        
      table.box = box.SIMPLE_HEAD
            
      table.add_column(" 解包", justify="center", no_wrap=True)
    
      table.add_column(" 打包", justify="center", no_wrap=True)
    
      table.title = (" 工程名称 > %s " % (self.Variable.rsplit('/', 1)[1]))
    
      for row in TABLE_DATA:
        table.add_row(*row)
    
      table.columns[0].style = "bright_cyan"
      table.columns[0].header_style = "bold cyan"
    
      table.columns[1].style = "bright_magenta"
      table.columns[1].header_style = "bold magenta"