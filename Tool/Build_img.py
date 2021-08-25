import subprocess, platform, magic
from Tool import Path
from Tool.Utility import Delete

class Build(object):
  def __init__(self,file, sdk=None):
    self.file = file
    self.img_file = str(self.file) + '.img'
    self.name = str(Path(self.file).name)
    self.dir = str(Path(self.file).parent)
    self.ContextsName = self.dir + '/config/' + self.name + '_new_file_contexts'
    self.ConfigName = self.dir + '/config/' + self.name + '_new_fs_config'
    self.Binary = Path(__file__).parent.absolute()
    self.szie = 0
    self.sdk = sdk


  def Size(self):
    if self.name == 'odm':
      self.size = int(Path(str(self.dir) + '/config/' + str(Path(self.name).name) + '_size.txt').open().read())
    elif self.name == 'product':
      self.size = 26 * 1024 * 1024
    elif self.name == 'system':
      self.size = 150 * 1024 * 1024
    elif self.name == 'vendor':
      self.size = 16 * 1024 * 1024
    elif self.name == 'system_ext':
      self.size = 16 * 1024 * 1024
    else:
      self.size = 20 * 1024 * 1024
    if self.name != 'odm':
      for file in Path(self.file).glob('**/*'):
        if file.is_symlink():
          self.size += file.lstat().st_size
        else:
          self.size += file.stat().st_size
    return self.size


  def Api(self):
    if not self.sdk:
      self.sdk = ['ro.' + self.name + '.build.version.sdk', 'ro.build.version.sdk']
    for file in Path(self.file).glob('**/build.prop'):
      conf = open(file).readlines()
      for configs in conf:
        if '=' in configs:
          config = configs.split('=')
          for con in self.sdk:
            if con == config[0]:
              return config[1].strip()
    return


  def __file_name(self, dirr):
    dirrs = dirr.replace('.', '\.')
    dirrs = dirrs.replace('+','\+')
    return dirrs


  def Generate_file(self):
    Contexts = self.dir + '/config/' + self.name + '_file_contexts'
    list = []
    selinux = open(Contexts, 'r').readlines()[0].split(' ')[1]


    with open(self.ContextsName, 'w') as cts:
      with open(self.ConfigName, 'w') as fs:
        if self.name == 'vendor':
          dir = '0 2000 0755\n'
        else:
          dir = '0 0 0755\n'


        fs.write('/ ' + dir)
        fs.write(self.name + ' ' + dir)
        cts.write('/ ' + selinux)
        cts.write('/' + self.name + '(/.*)? ' + selinux)
        cts.write('/' + self.name + ' ' + selinux)


        for file in Path(self.file).glob('**/*'):
          dirr = str(file).replace(self.dir, '')
          dirrs = str(file).replace(self.dir + '/', '')
          old = self.__file_name(dirr)
          if old in open(Contexts, 'r').read():
            for i in open(Contexts, 'r').readlines():
              if old == i.split(' ')[0]:
                cts.write(i)
          else:
            if 'system' in self.name:
              if str(self.name) + '/lib' in str(file):
                selinux = 'u:object_r:system_lib_file:s0'
            cts.write(old + ' ' + selinux)


          if file.is_dir():
            fs.write(dirrs + ' ' + dir)
          elif file.is_file():
            fs.write(dirrs + ' 0 0 0644\n')


  def Binarys(self):
    if platform.machine() == 'x86_64':
      self.conf = str(self.Binary) + '/Make/linux/mke2fs.conf'
      self.e2fsdroid = str(self.Binary) + '/Make/linux/e2fsdroid'
      self.mke2fs = str(self.Binary) + '/Make/linux/mke2fs'
      self.make_ext4fs = str(self.Binary) + '/Make/linux/make_ext4fs'
    else:
      self.conf = str(self.Binary) + '/Make/aarch64/mke2fs.conf'
      self.e2fsdroid = str(self.Binary) + '/Make/aarch64/e2fsdroid'
      self.mke2fs = str(self.Binary) + '/Make/aarch64/mke2fs'
      self.make_ext4fs = str(self.Binary) + '/Make/aarch64/make_ext4fs'


  def Dynamic(self)
    size = open(self.dir + '/config/' + str(Path(self.name).name) + '_size.txt').read()
    sz = 200 * 1024 * 1024
    new_size_1 = str(self.size + sz)
    old_file = str(self.dir) + '/dynamic_partitions_op_list'
    new_file = str(self.dir) + '/new_dynamic_partitions_op_list'
    old_str_1 = '# Grow partition ' + self.name + ' from 0 to ' + size
    old_str_2 = 'resize ' + self.name + ' ' + size
    file_data = ''


    with open(new_file, 'w', encoding='utf-8') as file:
      for line in open(old_file, 'r').readlines():
        if old_str_1 == line:
          lines = '# Grow partition ' + self.name + ' from 0 to ' + str(self.size) +'\n'
        elif old_str_2 == line:
          lines = 'resize ' + self.name + ' ' + new_size_1 +'\n'
        else:
          lines = line
        file_data += line
      file.write(file_data)
      Path(new_file).rename(old_file)

    Delete([self.ConfigName, self.ContextsName])


  def main(self):
    self.Size()
    self.Binarys()
    self.Generate_file()
    size = self.size // 4090
      
      # Mke2fa Generate empty image
    subprocess.run(['MKE2FS_CONFIG=' + self.conf + ' E2FSPROGS_FAKE_TIME=1230768000 ' + self.mke2fs + ' -O ^has_journal -L ' + self.name + ' -I 256 -M /' + self.name + ' -m 0 -t ext4 -b 4096 ' + self.img_file + ' ' + str(size)], shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)



    if Path(self.img_file).is_file():
      p = subprocess.run([self.e2fsdroid + ' -e -s -T 1230768000 -C ' + self.ConfigName + ' -S ' + self.ContextsName + ' -f ' + self.dir + '/' + self.name + '/ -a /' + self.name + ' ' + self.img_file],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)



      if 'sparse' not in magic.from_file(self.img_file):
        Sparse = self.img_file + 's'
        sparse = subprocess.run(['img2simg ' + self.img_file + ' ' + Sparse],shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        if not sparse.stderr.decode():
          Path(Sparse).rename(self.img_file)
          self.Dynamic()



      elif '__populate_fs:' in p.stderr.decode():
        print(p.stderr.decode())
        Path.unlink(Path(self.img_file))
        print('\033[1;31m[%s] 生成的 %s 空间不够大\033[0m\n' % (strftime('%H:%M:%S',localtime()), self.img_file))
        input('按任意键继续 ')
          
      elif p.stderr.decode():
        print('\033[1;31m[%s] 其他错误!\n%s\033[0m\n' % (strftime('%H:%M:%S',localtime()), p.stderr.decode().split('\n')[-2]))
        input('按任意键继续 ')

      
      # ext4fs Generate empty image
        #subprocess.run([self.make_ext4fs + ' -l ' + str(self.size) + ' -T 1230768000 -b 4096 -a ' + self.name + ' -S ' + self.ContextsName + '-C ' + self.ConfigName + ' ' + self.img_file + ' ' + self.file], shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
  