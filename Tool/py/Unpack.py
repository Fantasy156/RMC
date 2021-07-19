import time, functools, brotli
from rich.console import Console
from pathlib import Path

console = Console()
brea = '正在解压'
decompressor = brotli.Decompressor()

class Brotli(object):
  def __new__(self, File):
    console.print('\n[ %s ] %10s %s' % (time.strftime('%H:%M:%S',time.localtime()), brea, Path(File).name), style="bold cyan")
    size = Path(File).stat().st_size
    with open(str(File).rsplit('.', 1)[0], 'wb') as out_file:
      with open(str(File), 'rb') as in_file:
        try:
          if int(size) >= 2147483648:
            read_chunk = functools.partial(in_file.read, 4096)
            for data in iter(read_chunk, b''):
              out_file.write(decompressor.process(data))
          else:
            out_file.write(brotli.decompress(in_file.read()))
        except Exception as e:
          console.print('\n[ %s ] %10s' % (time.strftime('%H:%M:%S',time.localtime()), e), style="bold red")
          Path.unlink(Path(str(str(File).rsplit('.', 1)[0])))
    if Path(str(File).rsplit('.', 1)[0]).is_file():
        Path.unlink(Path(str(File)))
        
class Decompress(object):
  def __init__(self, File, Unpack=None):
    if Unpack == 'br':
      Brotli(File)