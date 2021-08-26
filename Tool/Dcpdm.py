import brotli, os, struct, traceback, re, mmap, string, tempfile
from Tool import Console, partial, Path, strftime, localtime, shutil, ext4, blockimgdiff, sparse_img
from Tool.Utility import Delete, Directory_Path, Mkdir
from Tool.Build_img import Build
from rich.progress import (
  BarColumn,
  DownloadColumn,
  Progress,
  TaskID,
  TextColumn,
  TimeRemainingColumn,
  TransferSpeedColumn,
  )
  
progress = Progress(
  TextColumn("[bold spring_green3]{task.fields[filename]}", justify="right"),
  BarColumn(bar_width=None),
  "[progress.percentage]{task.percentage:>0.1f}%",
  "•",
  DownloadColumn(),
  "•",
  TransferSpeedColumn(),
  "·",
  TimeRemainingColumn(),
  )

console = Console()

bkd = '正在分解'
stsz = '正在合成'

EXT4_HEADER_MAGIC = 0xED26FF3A
EXT4_SPARSE_HEADER_LEN = 28
EXT4_CHUNK_HEADER_SIZE = 12

class ext4_file_header(object):
    def __init__(self, buf):
        (self.magic,
         self.major,
         self.minor,
         self.file_header_size,
         self.chunk_header_size,
         self.block_size,
         self.total_blocks,
         self.total_chunks,
         self.crc32) = struct.unpack('<I4H4I', buf)


class ext4_chunk_header(object):
    def __init__(self, buf):
        (self.type,
         self.reserved,
         self.chunk_size,
         self.total_size) = struct.unpack('<2H2I', buf)


class Extractor(object):
    def __init__(self):
        self.FileName = ""
        self.OUTPUT_IMAGE_FILE = ""
        self.EXTRACT_DIR = ""
        self.BLOCK_SIZE = 4096
        self.TYPE_IMG = 'system'
        self.context = []
        self.fsconfig = []

    def __remove(self, path):
        if os.path.isfile(path):
            os.remove(path)  # remove the file
        elif os.path.isdir(path):
            shutil.rmtree(path)  # remove dir and all contains
        else:
            raise ValueError("file {} is not a file or dir.".format(path))

    def __logtb(self, ex, ex_traceback=None):
        if ex_traceback is None:
            ex_traceback = ex.__traceback__
        tb_lines = [line.rstrip('\n') for line in
                    traceback.format_exception(ex.__class__, ex, ex_traceback)]
        return '\n'.join(tb_lines)


    def __appendf(self, msg, log_file):
        with open(log_file, 'a', newline='\n') as file:
            print(msg, file=file)

    def __getperm(self, arg):
        if len(arg) < 9 or len(arg) > 10:
            return
        if len(arg) > 8:
            arg = arg[1:]
        oor, ow, ox, gr, gw, gx, wr, ww, wx = list(arg)
        o, g, w, s = 0, 0, 0, 0
        if oor == 'r': o += 4
        if ow == 'w': o += 2
        if ox == 'x': o += 1
        if ox == 'S': s += 4
        if ox == 's': s += 4; o += 1
        if gr == 'r': g += 4
        if gw == 'w': g += 2
        if gx == 'x': g += 1
        if gx == 'S': s += 2
        if gx == 's': s += 2; g += 1
        if wr == 'r': w += 4
        if ww == 'w': w += 2
        if wx == 'x': w += 1
        if wx == 'T': s += 1
        if wx == 't': s += 1; w += 1
        return str(s) + str(o) + str(g) + str(w)
        
    def __ext4extractor(self):
        fuking_symbols='\\^$.|?*+(){}[]'
        def scan_dir(root_inode, root_path=""):
            for entry_name, entry_inode_idx, entry_type in root_inode.open_dir():
                if entry_name in ['.', '..'] or entry_name.endswith(' (2)'):
                    continue
                entry_inode = root_inode.volume.get_inode(entry_inode_idx, entry_type)
                entry_inode_path = root_path + '/' + entry_name
                mode = self.__getperm(entry_inode.mode_str)
                uid = entry_inode.inode.i_uid
                gid = entry_inode.inode.i_gid
                con = ''
                cap = ''
                for i in list(entry_inode.xattrs()):
                    if i[0] == 'security.selinux':
                        con = i[1].decode('utf8')[:-1]
                    elif i[0] == 'security.capability':
                        raw_cap = struct.unpack("<5I", i[1])
                        if raw_cap[1] > 65535:
                            cap = '' + str(hex(int('%04x%04x' % (raw_cap[3], raw_cap[1]), 16)))
                        else:
                            cap = '' + str(hex(int('%04x%04x%04x' % (raw_cap[3], raw_cap[2], raw_cap[1]), 16)))
                        cap = ' capabilities={cap}'.format(cap=cap)
                if entry_inode.is_dir:
                    dir_target = self.EXTRACT_DIR + entry_inode_path.replace(' ','_')
                    if not os.path.isdir(dir_target):
                        os.makedirs(dir_target)
                    if os.name == 'posix':
                        os.chmod(dir_target, int(mode, 8))
                        os.chown(dir_target, uid, gid)
                    scan_dir(entry_inode, entry_inode_path)
                    if cap == '' and con == '':
                        tmppath=str(self.DIR) + entry_inode_path
                        if (tmppath).find(' ',1,len(tmppath))>0:
                            if not self.file_spaces.is_file:
                                f = open(self.file_spaces, 'tw', encoding='utf-8')
                                self.__appendf(tmppath, self.file_spaces)
                                f.close
                            else:
                                self.__appendf(tmppath, self.file_spaces)
                            tmppath=tmppath.replace(' ', '_')
                            self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode))
                        else:    
                            self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode))
                    else:
                        if cap == '':
                            tmppath=str(self.DIR) + entry_inode_path
                            if (tmppath).find(' ',1,len(tmppath))>0:
                                if not self.file_spaces.is_file:
                                    f = open(self.file_spaces, 'tw', encoding='utf-8')
                                    self.__appendf(tmppath, self.file_spaces)
                                    f.close
                                else:
                                    self.__appendf(tmppath, self.file_spaces)
                                tmppath=tmppath.replace(' ', '_')
                                self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode))
                            else:    
                                self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode))
                            for fuk_symb in fuking_symbols:
                                tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                            self.context.append('/%s %s' % (tmppath, con))
                        else:
                            if con == '':
                                tmppath=str(self.DIR) + entry_inode_path
                                if (tmppath).find(' ',1,len(tmppath))>0:
                                    if not self.file_spaces.is_file:
                                        f = open(self.file_spaces, 'tw', encoding='utf-8')
                                        self.__appendf(tmppath, self.file_spaces)
                                        f.close
                                    else:
                                        self.__appendf(tmppath, self.file_spaces)
                                    tmppath=tmppath.replace(' ', '_')
                                    self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode + cap))
                                else:    
                                    self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap))
                            else:
                                tmppath=str(self.DIR) + entry_inode_path
                                if (tmppath).find(' ',1,len(tmppath))>0:
                                    if not self.file_spaces.is_file:
                                        f = open(self.file_spaces, 'tw', encoding='utf-8')
                                        self.__appendf(tmppath, self.file_spaces)
                                        f.close
                                    else:
                                        self.__appendf(tmppath, self.file_spaces)
                                    tmppath=tmppath.replace(' ', '_')
                                    self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode + cap))
                                else:    
                                    self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap))
                                for fuk_symb in fuking_symbols:
                                    tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                                self.context.append('/%s %s' % (tmppath, con))
                elif entry_inode.is_file:
                    raw = entry_inode.open_read().read()
                    wdone = None
                    if os.name == 'nt':
                        if entry_name.endswith('/'):
                            entry_name = entry_name[:-1]
                        file_target = self.EXTRACT_DIR + entry_inode_path.replace('/', os.sep).replace(' ','_')
                        if not os.path.isdir(os.path.dirname(file_target)):
                            os.makedirs(os.path.dirname(file_target))
                        with open(file_target, 'wb') as out:
                            out.write(raw)
                    if os.name == 'posix':
                        file_target = self.EXTRACT_DIR + entry_inode_path.replace(' ','_')
                        if not os.path.isdir(os.path.dirname(file_target)):
                            os.makedirs(os.path.dirname(file_target))
                        with open(file_target, 'wb') as out:
                            out.write(raw)
                        os.chmod(file_target, int(mode, 8))
                        os.chown(file_target, uid, gid)
                    if cap == '' and con == '':
                        tmppath=str(self.DIR) + entry_inode_path
                        if (tmppath).find(' ',1,len(tmppath))>0:
                            if not self.file_spaces.is_file:
                                f = open(self.file_spaces, 'tw', encoding='utf-8')
                                self.__appendf(tmppath, self.file_spaces)
                                f.close
                            else:
                                self.__appendf(tmppath, self.file_spaces)
                            tmppath=tmppath.replace(' ', '_')
                            self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode))
                        else:    
                            self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode))
                    else:
                        if cap == '':
                            tmppath=str(self.DIR) + entry_inode_path
                            if (tmppath).find(' ',1,len(tmppath))>0:
                                if not self.file_spaces.is_file:
                                    f = open(self.file_spaces, 'tw', encoding='utf-8')
                                    self.__appendf(tmppath, self.file_spaces)
                                    f.close
                                else:
                                    self.__appendf(tmppath, self.file_spaces)
                                tmppath=tmppath.replace(' ', '_')
                                self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode))
                            else:    
                                self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode))
                            for fuk_symb in fuking_symbols:
                                tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                            self.context.append('/%s %s' % (tmppath, con))
                        else:
                            if con == '':
                                tmppath=str(self.DIR) + entry_inode_path
                                if (tmppath).find(' ',1,len(tmppath))>0:
                                    if not self.file_spaces.is_file:
                                        f = open(self.file_spaces, 'tw', encoding='utf-8')
                                        self.__appendf(tmppath, self.file_spaces)
                                        f.close
                                    else:
                                        self.__appendf(tmppath, self.file_spaces)
                                    tmppath=tmppath.replace(' ', '_')
                                    self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode + cap))
                                else:    
                                    self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap))
                            else:
                                tmppath=str(self.DIR) + entry_inode_path
                                if (tmppath).find(' ',1,len(tmppath))>0:
                                    if not self.file_spaces.is_file:
                                        f = open(self.file_spaces, 'tw', encoding='utf-8')
                                        self.__appendf(tmppath, self.file_spaces)
                                        f.close
                                    else:
                                        self.__appendf(tmppath, self.file_spaces)
                                    tmppath=tmppath.replace(' ', '_')
                                    self.fsconfig.append('%s %s %s %s' % (tmppath, uid, gid, mode + cap))
                                else:    
                                    self.fsconfig.append('%s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap))
                                for fuk_symb in fuking_symbols:
                                    tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                                self.context.append('/%s %s' % (tmppath, con))
                elif entry_inode.is_symlink:
                    try:
                        link_target = entry_inode.open_read().read().decode("utf8")
                        self.target = self.EXTRACT_DIR + entry_inode_path.replace(' ', '_')
                        if cap == '' and con == '':
                            tmppath=str(self.DIR) + entry_inode_path
                            if (tmppath).find(' ',1,len(tmppath))>0:
                                if not self.file_spaces.is_file:
                                    f = open(self.file_spaces, 'tw', encoding='utf-8')
                                    self.__appendf(tmppath, self.file_spaces)
                                    f.close
                                else:
                                    self.__appendf(tmppath, self.file_spaces)
                                tmppath=tmppath.replace(' ', '_')
                                self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode, link_target))
                            else:    
                                self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode, link_target))
                        else:
                            if cap == '':
                                tmppath=str(self.DIR) + entry_inode_path
                                if (tmppath).find(' ',1,len(tmppath))>0:
                                    if not self.file_spaces.is_file:
                                        f = open(self.file_spaces, 'tw', encoding='utf-8')
                                        self.__appendf(tmppath, self.file_spaces)
                                        f.close
                                    else:
                                        self.__appendf(tmppath, self.file_spaces)
                                    tmppath=tmppath.replace(' ', '_')
                                    self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode, link_target))
                                else:    
                                    self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode, link_target))
                                for fuk_symb in fuking_symbols:
                                    tmppath=tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                                self.context.append('/%s %s' % (tmppath, con))
                            else:
                                if con == '':
                                    tmppath=str(self.DIR) + entry_inode_path
                                    if (tmppath).find(' ',1,len(tmppath))>0:
                                        if not self.file_spaces.is_file:
                                            f = open(self.file_spaces, 'tw', encoding='utf-8')
                                            self.__appendf(tmppath, self.file_spaces)
                                            f.close
                                        else:
                                            self.__appendf(tmppath, self.file_spaces)
                                        tmppath=tmppath.replace(' ', '_')
                                        self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode + cap, link_target))
                                    else:    
                                        self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap, link_target))
                                else:
                                    tmppath=str(self.DIR) + entry_inode_path
                                    if (tmppath).find(' ',1,len(tmppath))>0:
                                        if not self.file_spaces.is_file:
                                            f = open(self.file_spaces, 'tw', encoding='utf-8')
                                            self.__appendf(tmppath, self.file_spaces)
                                            f.close
                                        else:
                                            self.__appendf(tmppath, self.file_spaces)
                                        tmppath=tmppath.replace(' ', '_')
                                        self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode + cap, link_target))
                                    else:    
                                        self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap, link_target))
                                    for fuk_symb in fuking_symbols:
                                        tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                                    self.context.append('/%s %s' % (tmppath, con))
                        if os.path.islink(self.target):
                            try:
                                os.remove(self.target)
                            except:
                                pass
                        if os.path.isfile(self.target):
                            try:
                                os.remove(self.target)
                            except:
                                pass
                        if os.name == 'posix':
                            os.symlink(link_target, self.target)
                        if os.name == 'nt':
                            with open(self.target.replace('/', os.sep), 'wb') as out:
                                tmp = bytes.fromhex('213C73796D6C696E6B3EFFFE')
                                for index in list(link_target):
                                    tmp = tmp + struct.pack('>sx', index.encode('utf-8'))
                                out.write(tmp + struct.pack('xx'))
                                os.system('attrib +s "%s"' % self.target.replace('/', os.sep))
                        if not all(c in string.printable for c in link_target):
                            pass
                        if entry_inode_path[1:] == entry_name or link_target[1:] == entry_name:
                            self.symlinks.append('%s %s' % (link_target, entry_inode_path[1:]))
                        else:
                            self.symlinks.append('%s %s' % (link_target, str(self.DIR) + entry_inode_path))
                    except:
                        try:
                            link_target_block = int.from_bytes(entry_inode.open_read().read(), "little")
                            link_target = root_inode.volume.read(link_target_block * root_inode.volume.block_size, entry_inode.inode.i_size).decode("utf8")
                            self.target = self.EXTRACT_DIR + entry_inode_path.replace(' ', '_')
                            if link_target and all(c in string.printable for c in link_target):
                                if cap == '' and con == '':
                                    tmppath=str(self.DIR) + entry_inode_path
                                    if (tmppath).find(' ',1,len(tmppath))>0:
                                        if not self.file_spaces.is_file:
                                            f = open(self.file_spaces, 'tw', encoding='utf-8')
                                            self.__appendf(tmppath, self.file_spaces)
                                            f.close
                                        else:
                                            self.__appendf(tmppath, self.file_spaces)
                                        tmppath=tmppath.replace(' ', '_')
                                        self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode, link_target))
                                    else:    
                                        self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode, link_target))
                                else:
                                    if cap == '':
                                        tmppath=str(self.DIR) + entry_inode_path
                                        if (tmppath).find(' ',1,len(tmppath))>0:
                                            if not self.file_spaces.is_file:
                                                f = open(self.file_spaces, 'tw', encoding='utf-8')
                                                self.__appendf(tmppath, self.file_spaces)
                                                f.close
                                            else:
                                                self.__appendf(tmppath, self.file_spaces)
                                            tmppath=tmppath.replace(' ', '_')
                                            self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode, link_target))
                                        else:    
                                            self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode, link_target))
                                        for fuk_symb in fuking_symbols:
                                            tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                                        self.context.append('/%s %s' % (tmppath, con))
                                    else:
                                        if con == '':
                                            tmppath=str(self.DIR) + entry_inode_path
                                            if (tmppath).find(' ',1,len(tmppath))>0:
                                                if not self.file_spaces.is_file:
                                                    f = open(self.file_spaces, 'tw', encoding='utf-8')
                                                    self.__appendf(tmppath, self.file_spaces)
                                                    f.close
                                                else:
                                                    self.__appendf(tmppath, self.file_spaces)
                                                tmppath=tmppath.replace(' ', '_')
                                                self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode + cap, link_target))
                                            else:    
                                                self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap, link_target))
                                        else:
                                            tmppath=str(self.DIR) + entry_inode_path
                                            if (tmppath).find(' ',1,len(tmppath))>0:
                                                if not self.file_spaces.is_file:
                                                    f = open(self.file_spaces, 'tw', encoding='utf-8')
                                                    self.__appendf(tmppath, self.file_spaces)
                                                    f.close
                                                else:
                                                    self.__appendf(tmppath, self.file_spaces)
                                                tmppath=tmppath.replace(' ', '_')
                                                self.fsconfig.append('%s %s %s %s %s' % (tmppath, uid, gid, mode + cap, link_target))
                                            else:    
                                                self.fsconfig.append('%s %s %s %s %s' % (str(self.DIR) + entry_inode_path, uid, gid, mode + cap, link_target))
                                            for fuk_symb in fuking_symbols:
                                                tmppath=tmppath.replace(fuk_symb, '\\'+fuk_symb)
                                            self.context.append('/%s %s' % (tmppath, con))
                                if os.name == 'posix':
                                    os.symlink(link_target, target)
                                if os.name == 'nt':
                                    with open(self.target.replace('/', os.sep), 'wb') as out:
                                        tmp = bytes.fromhex('213C73796D6C696E6B3EFFFE')
                                        for index in list(link_target):
                                            tmp = tmp + struct.pack('>sx', index.encode('utf-8'))
                                        out.write(tmp + struct.pack('xx'))
                                        os.system('attrib +s %s' % self.target.replace('/', os.sep))
                            else:
                                pass
                        except:
                            pass
                            
        if not os.path.isdir(self.configname):
            os.mkdir(self.configname)
       # f = open(self.configname + self.FileName + '_pack.sh', 'tw', encoding='utf-8')
       # self.__appendf('make_ext4fs -T -1 -S ./file_contexts -C ./fs_config -l ' +str(os.path.getsize(self.OUTPUT_IMAGE_FILE))+ ' -a /'+self.FileName+' "$outdir"/'+self.FileName+'.new.img '+self.FileName+'', self.configname + self.FileName + '_pack.sh')
       # f.close()
       # f = open(self.configname + self.FileName + '_pack_sparse.sh', 'tw', encoding='utf-8')
       # self.__appendf('make_ext4fs -s -T -1 -S ./file_contexts -C ./fs_config -l ' +str(os.path.getsize(self.OUTPUT_IMAGE_FILE))+ ' -a /'+self.FileName+' "$outdir"/'+self.FileName+'.new.img '+self.FileName+'', self.configname + self.FileName + '_pack_sparse.sh')
       # f.close()
        f = open(self.file_size, 'tw', encoding='utf-8')
        self.__appendf(os.path.getsize(self.OUTPUT_IMAGE_FILE), self.file_size)
        f.close()
       # f = open(self.configname + self.FileName + '_name.txt', 'tw', encoding='utf-8')
       # self.__appendf(os.path.basename(self.OUTPUT_IMAGE_FILE).replace(".img", ""), self.configname + self.FileName + '_name.txt')
       # f.close()
        with open(self.OUTPUT_IMAGE_FILE, 'rb') as file:
            root = ext4.Volume(file).root
            dirlist = []
            for file_name, inode_idx, file_type in root.open_dir():
                dirlist.append(file_name)
            dirr = self.FileName
            setattr(self, 'DIR', dirr)
            scan_dir(root)          
            for c in self.fsconfig:
                if dirr == 'vendor':
                    self.fsconfig.insert(0, '/' + ' 0 2000 0755')
                    self.fsconfig.insert(1, dirr + ' 0 2000 0755')
                elif dirr == 'system':
                    self.fsconfig.insert(0, '/' + ' 0 0 0755')
                    self.fsconfig.insert(1, '/' + 'lost+found' + ' 0 0 0700')
                    self.fsconfig.insert(2, dirr + ' 0 0 0755')
                else:
                    self.fsconfig.insert(0, '/' + ' 0 0 0755')
                    self.fsconfig.insert(1, dirr + ' 0 0 0755')
                break 

            self.__appendf('\n'.join(self.fsconfig),self.file_config)
            if self.context: #11.05.18
                self.context.sort() #11.05.18
                for c in self.context:
                    if re.search('lost..found', c):
                        self.context.insert(0, '/' + ' ' + c.split(" ")[1])                    
                        self.context.insert(1, '/' + dirr +'(/.*)? ' + c.split(" ")[1])
                        self.context.insert(2, '/' + dirr + ' ' + c.split(" ")[1])
                        self.context.insert(3, '/' + dirr + '/lost\+found' + ' ' + c.split(" ")[1])
                        break
                for c in self.context:
                    if re.search('/system/system/build..prop ', c):
                        self.context.insert(3, '/lost\+found' + ' u:object_r:rootfs:s0')
                        self.context.insert(4, '/' + dirr + '/' + dirr + '(/.*)? ' + c.split(" ")[1])
                        break
                self.__appendf('\n'.join(self.context), self.file_contexts) #11.05.18

    def __converSimgToImg(self):
        with open(self.target, "rb") as img_file:
            if self.sign_offset > 0:
                img_file.seek(self.sign_offset, 0)
            header = ext4_file_header(img_file.read(28))
            total_chunks = header.total_chunks
            if header.file_header_size > EXT4_SPARSE_HEADER_LEN:
                img_file.seek(header.file_header_size - EXT4_SPARSE_HEADER_LEN, 1)
            with open(self.target.replace(".img", ".raw.img"), "wb") as raw_img_file:
                sector_base = 82528
                output_len = 0
                while total_chunks > 0:
                    chunk_header = ext4_chunk_header(img_file.read(EXT4_CHUNK_HEADER_SIZE))
                    sector_size = (chunk_header.chunk_size * header.block_size) >> 9
                    chunk_data_size = chunk_header.total_size - header.chunk_header_size
                    if chunk_header.type == 0xCAC1:  # CHUNK_TYPE_RAW
                        if header.chunk_header_size > EXT4_CHUNK_HEADER_SIZE:
                            img_file.seek(header.chunk_header_size - EXT4_CHUNK_HEADER_SIZE, 1)
                        data = img_file.read(chunk_data_size)
                        len_data = len(data)
                        if len_data == (sector_size << 9):
                            raw_img_file.write(data)
                            output_len += len_data
                            sector_base += sector_size
                    else:
                        if chunk_header.type == 0xCAC2:  # CHUNK_TYPE_FILL
                            if header.chunk_header_size > EXT4_CHUNK_HEADER_SIZE:
                                img_file.seek(header.chunk_header_size - EXT4_CHUNK_HEADER_SIZE, 1)
                            data = img_file.read(chunk_data_size)
                            len_data = sector_size << 9
                            raw_img_file.write(struct.pack("B", 0) * len_data)
                            output_len += len(data)
                            sector_base += sector_size
                        else:
                            if chunk_header.type == 0xCAC3:  # CHUNK_TYPE_DONT_CARE
                                if header.chunk_header_size > EXT4_CHUNK_HEADER_SIZE:
                                    img_file.seek(header.chunk_header_size - EXT4_CHUNK_HEADER_SIZE, 1)
                                data = img_file.read(chunk_data_size)
                                len_data = sector_size << 9
                                raw_img_file.write(struct.pack("B", 0) * len_data)
                                output_len += len(data)
                                sector_base += sector_size
                            else:
                                len_data = sector_size << 9
                                raw_img_file.write(struct.pack("B", 0) * len_data)
                                sector_base += sector_size
                    total_chunks -= 1
        self.OUTPUT_IMAGE_FILE = self.target.replace(".img", ".raw.img")
    
    def fixmoto(self, input_file):
        if os.path.exists(input_file) == False:
            return
        output_file=input_file + "_"
        if os.path.exists(output_file) == True:
            try:
                os.remove(output_file)
            except:
                pass
        with open(input_file, 'rb') as f:
            data = f.read(500000)
        moto = re.search(b'\x4d\x4f\x54\x4f', data)
        if not moto:
            return
        result = []
        for i in re.finditer(b'\x53\xEF', data):
            result.append(i.start() - 1080)
        offset = 0
        for i in result:
            if data[i] == 0:
                offset = i
                break        
        if offset > 0:
            with open(output_file, 'wb') as o, open(input_file, 'rb') as f:
                data = f.seek(offset)
                data = f.read(15360)
                while data:
                    devnull = o.write(data)
                    data = f.read(15360)
        try:
                os.remove(input_file)
                os.rename(output_file, input_file)
        except:
                pass
    def checkSignOffset(self, file):
        size=os.stat(file.name).st_size
        if size <= 52428800:
            mm = mmap.mmap(file.fileno(),0 , access=mmap.ACCESS_READ)
        else:
            mm = mmap.mmap(file.fileno(),52428800 , access=mmap.ACCESS_READ)  # 52428800=50Mb
        offset = mm.find(struct.pack('<L', EXT4_HEADER_MAGIC))
        return offset

    def __getTypeTarget(self, target):
        filename, file_extension = os.path.splitext(target)
        if file_extension == '.img':
            with open(target, "rb") as img_file:
                setattr(self, 'sign_offset', self.checkSignOffset(img_file))
                if self.sign_offset > 0:
                    img_file.seek(self.sign_offset, 0)
                header = ext4_file_header(img_file.read(28))
                if header.magic != EXT4_HEADER_MAGIC:
                    return 'img'
                else:
                    return 'simg'

    def main(self, target, output_dir):
        self.configname = str(output_dir) + '/config/'
        self.OUTPUT_IMAGE_FILE = target
        self.OUTPUT_MYIMAGE_FILE = str(Path(target).name)
        self.FileName = str(Path(target).stem)
        self.EXTRACT_DIR = str(output_dir) + '/' + self.FileName
        self.file_contexts = Path(self.configname + self.FileName + '_file_contexts')
        self.file_config = Path(self.configname + self.FileName + '_fs_config')
        self.file_size = Path(self.configname + self.FileName + '_size.txt')
        self.file_spaces = Path(self.configname + self.FileName + '_space.txt')
        target_type = self.__getTypeTarget(target)
        if target_type == 'simg':
            self.__converSimgToImg(target)
            with open(self.OUTPUT_IMAGE_FILE, 'rb') as f:
                data = f.read(500000)
            moto = re.search(b'\x4d\x4f\x54\x4f', data)
            if moto:
                self.fixmoto(self.OUTPUT_IMAGE_FILE)
            self.__ext4extractor()
        if target_type == 'img':
            with open(self.OUTPUT_IMAGE_FILE, 'rb') as f:
                data = f.read(500000)
            moto = re.search(b'\x4d\x4f\x54\x4f', data)
            if moto:
                self.fixmoto(self.OUTPUT_IMAGE_FILE)
            self.__ext4extractor()
        Delete(target)


class Img(object):
  def __init__(self, file):
    self.file = file
    self.img_file = Path(self.file + '.img')
    self.dir = Path(self.file).parent


  def Pack(self):
    if self.img_file.is_file():
      Delete(self.img_file)
    img = Build(self.file)
    size = img.Size()
    Api = img.Api()
    if not Api:
      return
    console.print('\n[ %s ] %10s %s <Api:%s Size: %s Type:Sparse>' % (strftime('%H:%M:%S',localtime()), stsz, self.img_file.name, Api, size), style="bold cyan")    
    img.main()
    return Api


  def Unpack(self):
    if self.img_file.is_file:
      Delete(self.file)
      console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), bkd, self.img_file.name), style="bold cyan")
      Extractor().main(self.img_file, self.dir)
      


class Dat(object):
  def __init__(self, file):
    self.file = file
    self.BLOCK_SIZE = 4096
    self.dat_file = Path(self.file + '.new.dat')
    self.img_file = Path(self.file + '.img')
    self.transfer = Path(self.file + '.transfer.list')
    self.patch = Path(self.file + '.patch.dat')
    self.progress = Progress(
  TextColumn("[bold spring_green3]{task.fields[filename]}", justify="right"),
  BarColumn(bar_width=None),
  "[progress.percentage]{task.percentage:>0.1f}%",
  "•",
  DownloadColumn(),
  "•",
  TransferSpeedColumn(),
  "·",
  TimeRemainingColumn(),
  )


  def rangeset(self, src):
      src_set = src.split(',')
      num_set =  [int(item) for item in src_set]
      if len(num_set) != num_set[0]+1:
        console.print('将以下数据解析为范围集时出错:\n{}'.format(src), file=sys.stderr, style="bold red")
        Delete(self.img_file)
        input('按任意键继续: ')
      return tuple ([ (num_set[i], num_set[i+1]) for i in range(1, len(num_set), 2) ])
 

  def parse_transfer_list_file(self, path):
      with open(self.transfer, 'r') as trans_list:
        version = int(trans_list.readline())   
        new_blocks = int(trans_list.readline())
        commands = []
        for line in trans_list:      
          line = line.split(' ')
          cmd = line[0]
          if cmd in ['erase', 'new', 'zero']:
            commands.append([cmd, self.rangeset(line[1])])
          else:
            if not cmd[0].isdigit():
              print('命令 "{}" 无效.'.format(cmd), file=sys.stderr, style="bold red")
              input()
              return
        return version, new_blocks, commands


  def Pack(self):
    if self.dat_file.is_file():
      Delete(self.dat_file)
    Api = Img(self.file).Pack()
    if self.img_file.is_file():
      OUTDIR = str(self.file)
      VERSION = 4
      console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), stsz, self.dat_file.name), style="bold cyan")
      image = sparse_img.SparseImage(str(self.img_file), tempfile.mkstemp()[1], '0')
     # image = str(self.img_file)
      b = blockimgdiff.BlockImageDiff(image, None, VERSION)
      b.Compute(OUTDIR)
      if self.dat_file.is_file():
        Delete([self.img_file])


  def Unpack(self):
    if self.dat_file.is_file():
      Delete(self.img_file)
      console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), bkd, self.dat_file.name), style="bold cyan")
      size = self.dat_file.stat().st_size
      version, new_blocks, commands = self.parse_transfer_list_file(self.transfer)
      with self.progress:
        task_id = self.progress.add_task('decompress', filename=self.dat_file.name, start=False)
        self.progress.update(task_id, total=size)
        with open(self.img_file, 'wb') as output_img:
          with open(self.dat_file, 'rb') as new_data_file:
            all_block_sets = [i for command in commands for i in command[1]]
            max_file_size = max(pair[1] for pair in all_block_sets)*self.BLOCK_SIZE    
            for command in commands:
              if command[0] == 'new':
                for block in command[1]:
                  begin = block[0]
                  end = block[1]
                  block_count = end - begin
                  output_img.seek(begin*self.BLOCK_SIZE)
                  while(block_count > 0):
                    self.progress.start_task(task_id)
                    output_img.write(new_data_file.read(self.BLOCK_SIZE))
                    self.progress.update(task_id, advance=self.BLOCK_SIZE)
                    block_count -= 1
            if(output_img.tell() < max_file_size):
              output_img.truncate(max_file_size)
      Delete([self.dat_file, self.transfer, self.patch])
      Img(self.file).Unpack()


class Brotli(object):
  def __init__(self, file):
    self.file = file
    self.br_file = Path(self.file + '.new.dat.br')
    self.dat_file = Path(self.file + '.new.dat')
    self.chunk_size = 4096
    self.quality = 5
    self.decompressor = brotli.Decompressor()
    self.compressor = brotli.Compressor(quality=self.quality)
    self.progress = Progress(
  TextColumn("[bold spring_green3]{task.fields[filename]}", justify="right"),
  BarColumn(bar_width=None),
  "[progress.percentage]{task.percentage:>0.1f}%",
  "•",
  DownloadColumn(),
  "•",
  TransferSpeedColumn(),
  "·",
  TimeRemainingColumn(),
  )
    
    
  def sec(self, file):
    self.compressor = None
    self.decompressor = None
    Delete(file)
 

  def Pack(self):
    if self.br_file.is_file():
      Delete(self.br_file)
    Dat(self.file).Pack()
    if self.dat_file.is_file():
      console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), stsz, self.br_file.name), style="bold cyan")
      size = self.dat_file.stat().st_size
      with self.progress:
        task_id = self.progress.add_task('decompress', filename=self.dat_file.name, start=False)
        self.progress.update(task_id, total=size)
        with open(self.br_file, 'wb') as out_file:
          with open(self.dat_file, 'rb') as in_file:
            try:
              for data in iter(partial(in_file.read, self.chunk_size), b''):
                self.progress.start_task(task_id)
                out_file.write(self.compressor.process(data))
                self.progress.update(task_id, advance=self.chunk_size)
            except Exception as e:
              console.print('\n[ %s ] %10s' % (strftime('%H:%M:%S',localtime()), e), style="bold red")
          out_file.write(self.compressor.finish())
      self.sec(self.dat_file)

 
  def Unpack(self):
    if self.br_file.is_file:
      Delete(self.dat_file)
      console.print('\n[ %s ] %10s %s' % (strftime('%H:%M:%S',localtime()), bkd, self.br_file.name), style="bold cyan")
      size = self.br_file.stat().st_size
      with self.progress:
        task_id = self.progress.add_task('decompress', filename=self.br_file.name, start=False)
        self.progress.update(task_id, total=size)
        with open(self.dat_file, 'wb') as out_file:
          with open(self.br_file, 'rb') as in_file:
            try:
              for data in iter(partial(in_file.read, self.chunk_size), b''):
                self.progress.start_task(task_id)
                out_file.write(self.decompressor.process(data))
                self.progress.update(task_id, advance=self.chunk_size)
            except Exception as e:
              console.print('\n[ %s ] %10s' % (strftime('%H:%M:%S',localtime()), e), style="bold red")
      self.sec(self.br_file)
      Dat(self.file).Unpack()


    
class Task(object):
  def __init__(self, PROJECT, Task, name=None):
    self.task = Task
    self.project = PROJECT
    self.name = name


  def Unpack(self):
      files = Directory_Path(Path(self.project), '*').list()
      for f in files:
        if Path(f).is_file():
          try:
            file = self.project + '/' + str(Path(f).name).split('.', 1)[0]
          except Exception:
            pass
          if self.name == 'br':
            if Path(f).suffix == '.br':
              Brotli(file).Unpack()
          elif self.name == 'new.dat':
            if Path(f).suffix == '.dat' and '.new.dat' in f:
              Dat(file).Unpack()
          elif self.name == 'img':
            if Path(f).suffix == '.img':
              if Path(file).name != 'boot':
                Img(file).Unpack()
          else:
            if Path(f).suffix == '.br':
              Brotli(file).Unpack()
            elif Path(f).suffix == '.dat' and '.new.dat' in f:
              Dat(file).Unpack()
            elif Path(f).suffix == '.img':
              if Path(file).name != 'boot':
                Img(file).Unpack()
          


  def Pack(self):
    files = Directory_Path(Path(self.project), '*').list()
    for f in files:
      if Path(f).is_dir():
        ContextsName = str(self.project) + '/config/' + str(Path(f).name) + '_file_contexts'
        ConfigName = str(self.project) + '/config/' + str(Path(f).name) + '_fs_config'
        if Path(ContextsName).is_file():
          if Path(ConfigName).is_file():
            file = self.project + '/' + str(Path(f).name).split('.', 1)[0]
            if self.name == 'img':
              Img(file).Pack()
            elif self.name == 'dat':
              if Path(file).name != 'boot':
                Dat(file).Pack()
            elif self.name == 'br':
              Brotli(file).Pack()


  def main(self):
    if self.task == 'Unpack':
      self.Unpack()
    elif self.task == 'Pack':
      self.Pack()