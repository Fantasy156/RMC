from local.core import inputs
from local.dwonload import download
from local.utlity import download_dir
from local.utlity import table


def run(target):
    data = ['新建工程']
    styles = ['bright_cyan', 'bright_magenta']
    table(variable=data, header='RMC 解包工具', styles=styles)

    data = ['选择', '删除', '下载', '退出']
    number = [33, 44, 66, 88]
    styles = ['bright_cyan', 'bright_magenta']
    table(variable=data, styles=styles, number=number, num=len(data))

    url = inputs('输入链接')
    download(url, download_dir(target))
