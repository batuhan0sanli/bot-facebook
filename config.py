import json


class Config:
    def __init__(self, config_file='config.json'):
        self.config_file = config_file

        # Driver Options
        self.driver_path = None
        self.driver_headless = None
        self.driver_window_size = None
        self.driver_sleep_after_action = None
        self.driver_timeout = None

        # Find Element Options
        self.findElement_clickPosts = None
        self.findElement_closePopUpLogin = None
        self.findElement_AndWord = None
        self.findElement_timeline = None
        self.findElement_posts = None
        self.findElement_like = None
        self.findElement_comment = None
        self.findElement_share = None
        self.findElement_date = None

        self.__readFile()

    def __readFile(self):
        with open(self.config_file, 'r') as config_file:
            conf = json.load(config_file)
            self.driver_path = conf.get('driver_options').get('path')
            self.driver_headless = conf.get('driver_options').get('headless')
            self.driver_window_size = conf.get('driver_options').get('window_size')
            self.driver_sleep_after_action = conf.get('driver_options').get('sleep_after_action')
            self.driver_timeout = conf.get('driver_options').get('timeout')

            self.findElement_clickPosts = conf.get('find_element_options').get('text_click_posts')
            self.findElement_closePopUpLogin = conf.get('find_element_options').get('text_close_popUpLogin')
            self.findElement_AndWord = conf.get('find_element_options').get('text_and_word')
            self.findElement_timeline = conf.get('find_element_options').get('xpath_timeline')
            self.findElement_posts = conf.get('find_element_options').get('xpath_posts')
            self.findElement_like = conf.get('find_element_options').get('div_class_like')
            self.findElement_comment = conf.get('find_element_options').get('a_class_comment')
            self.findElement_share = conf.get('find_element_options').get('a_class_share')
            self.findElement_date = conf.get('find_element_options').get('type_date')
