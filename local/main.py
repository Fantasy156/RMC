import local.character as character
from itertools import repeat
from local.core import inputs, prints, back_, title
from local.dwonload import download
from local.tree import mkdir, find, delete
from local.utlity import table, zip_dir, project_dir


def function(project, directory, target):
    table(variable=character.project, header=title(chara=project),
          styles=character.styles, num=2)
    table(variable=character.project_choose, number=character.project_choose_number,
          styles=character.styles, num=len(character.project_choose))
    select = back_(inputs(character.choose))
    match select:
        case 0:
            for _ in repeat((None,)):
                run(target)
        case 1:
            pass
        case 2:
            pass
        case 3:
            pass
        case 4:
            pass
        case 5:
            pass
        case 6:
            pass
        case 7:
            pass
        case 8:
            pass
        case 9:
            pass
        case 77:
            pass
        case 88:
            exit(prints('退出【R M C】', style='bold red'))
        case _:
            pass


def rom_list(directory):
    data = find('*.zip', directory)
    table(variable=data, header=title(chara='选择刷机包'), styles=character.styles, start=1)
    table(variable=['返回上级'], styles=character.styles)
    select = back_(inputs(character.choose))
    match select:
        case None:
            delete_project()
        case 0:
            pass
        case _:
            delete(f'{project_dir()}/{data[select - 1]}') if select <= len(data) else None


def delete_project():
    data = find('Errors_*', project_dir())
    table(variable=data, header=title(chara='删除项目'), styles=character.styles, start=1)
    table(variable=['返回上级'], styles=character.styles)
    select = back_(inputs(character.choose))
    match select:
        case None:
            delete_project()
        case 0:
            pass
        case _:
            delete(f'{project_dir()}/{data[select-1]}') if select <= len(data) else None


def run(target):
    data = find('Errors_*', project_dir())
    table(variable=data, header=title(chara=character.tool_name), styles=character.styles, start=1)
    table(variable=character.home, styles=character.styles, number=character.home_number, num=len(character.home))
    select = back_(inputs(character.choose))
    match select:
        case None:
            pass
        case 00:
            prints('新建工程>\n', style='turquoise2')
            name = inputs('  输入名称【不能有空格, 特殊符号】: Errors_')
            mkdir(f'{project_dir()}/Errors_{name}')
        case 33:
            rom_list(zip_dir(target))
        case 44:
            delete_project()
        case 66:
            url = inputs('输入链接')
            download(url, zip_dir(target))
        case 88:
            exit(prints('退出【R M C】', style='bold red'))
        case _:
            for _ in repeat((None,)):
                function(data[select - 1], f'{project_dir()}/{data[select - 1]}', target)\
                    if select <= len(data) else None
