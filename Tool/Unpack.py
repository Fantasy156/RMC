import brotli
from Tool import Console, partial, Path, strftime, localtime
from Tool.Utility import Delete

console = Console()
brea = '正在解压'
decompressor = brotli.Decompressor()

class Sdat2img(object):
  def __new__(self, File):

    def rangeset(src):
      src_set = src.split(',')
      num_set =  [int(item) for item in src_set]

      if len(num_set) != num_set[0]+1:
        console.print('将以下数据解析为范围集时出错:\n{}'.format(src), file=sys.stderr, style="bold red")
        Delete(list=[out_files], veri=out_files)
        input('按任意键继续: ')

      return tuple ([ (num_set[i], num_set[i+1]) for i in range(1, len(num_set), 2) ])

    def parse_transfer_list_file(path):
      trans_list = open(transfer, 'r')
      version = int(trans_list.readline())   
      new_blocks = int(trans_list.readline())

      if version >= 2:
        trans_list.readline()       
        trans_list.readline()
       
      commands = []
      for line in trans_list:      
        line = line.split(' ')
        cmd = line[0]
        if cmd in ['erase', 'new', 'zero']:
          commands.append([cmd, rangeset(line[1])])

        else:
          if not cmd[0].isdigit():
            print('命令 "{}" 无效.'.format(cmd), file=sys.stderr, style="bold red")
            trans_list.close()
            Delete(list=[out_files], veri=out_files)
            input('按任意键继续: ')

      trans_list.close()
      return version, new_blocks, commands

    console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), brea, Path(File).name), style="bold cyan")

    path = str(File).rsplit('/', 1)[0]
    name = Path(File).name.split('.', 1)[0]
    transfer = path + '/' + name + '.transfer.list'
    out_file = path + '/' + name + '.img'
    patch = path + '/' + name + '.patch.dat'

    BLOCK_SIZE = 4096

    version, new_blocks, commands = parse_transfer_list_file(transfer)
    if Path(out_file).is_file():
      Path.unlink(Path(out_file))

    output_img = open(out_file, 'wb')
    new_data_file = open(str(File), 'rb')
    all_block_sets = [i for command in commands for i in command[1]]
    max_file_size = max(pair[1] for pair in all_block_sets)*BLOCK_SIZE
    
    for command in commands:
      if command[0] == 'new':
        for block in command[1]:
          begin = block[0]
          end = block[1]
          block_count = end - begin
          output_img.seek(begin*BLOCK_SIZE)

          while(block_count > 0):
            output_img.write(new_data_file.read(BLOCK_SIZE))
            block_count -= 1

    if(output_img.tell() < max_file_size):
      output_img.truncate(max_file_size)

    output_img.close()
    new_data_file.close()

    Delete(list=[str(File), transfer, patch], veri=out_file)    

class Brotli(object):
  def __new__(self, File):
    console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), brea, Path(File).name), style="bold cyan")

    size = Path(File).stat().st_size
    out_files = str(File).rsplit('.', 1)[0]

    with open(out_files, 'wb') as out_file:
      with open(str(File), 'rb') as in_file:

        try:
          if int(size) >= 2147483648:
            read_chunk = partial(in_file.read, 4096)

            for data in iter(read_chunk, b''):
              out_file.write(decompressor.process(data))

          else:
            out_file.write(brotli.decompress(in_file.read()))

        except Exception as e:
          console.print('\n[ %s ] %10s' % (strftime('%H:%M:%S',localtime()), e), style="bold red")
          Delete(list=[out_files])

    Delete(list=[str(File)], veri=out_files)

    Sdat2img(out_files)
        
class Decompress(object):
  def __init__(self, File, Unpack=None):
    if Unpack == 'br':
      Brotli(File)

    elif Unpack == 'dat':
      Sdat2img(File)

    input('按任意键继续: ')