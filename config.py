import json


class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file
        self.driver_path = None
        self.driver_headless = None
        self.driver_window_size = None
        self.__readFile()

    def __readFile(self):
        with open(self.config_file, 'r') as config_file:
            conf = json.load(config_file)
            self.driver_path = conf.get('driver_options').get('path')
            self.driver_headless = conf.get('driver_options').get('headless')
            self.driver_window_size = conf.get('driver_options').get('window_size')
