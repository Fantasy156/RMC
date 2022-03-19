import json
from pathlib import Path, PurePath

CONFIG_DICT = {
    'PC_BIN': 'PC_BIN',
    'AARCH64_BIN': 'AARCH64_BIN',
    'FILE_DIR': 'FILE_DIR',
    'THREAD': 'THREAD',
    'PROJECT_DIR': 'PROJECT_DIR'
}


class Config(object):
    def __init__(self):
        project_path = str(Path(__file__).parent.absolute())
        config_file = str(PurePath(project_path, 'config', 'config.json'))

        with open(config_file, 'r', encoding='utf-8') as f:
            self.config_json = json.load(f)

        for i in CONFIG_DICT:
            self.__dict__[i] = self.get_config(i)

    def get_config(self, key: str):
        value = self.config_json.get(key, '')

        return value


config = Config()
