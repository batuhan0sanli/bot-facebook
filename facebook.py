import hashlib
from __init__ import url_md5_csv
from config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


class Facebook:
    def __init__(self, url):
        self.url = url
        self.md5 = self.__get_md5()
        self.url_md5_csv = url_md5_csv

        # Config
        self.config = Config()

        # url-md5.csv
        self.__save_url_md5_csv()

        # Selenium
        self.driver = self.__set_driver()
        self.__get_url()
        self.__save_main_screenshot()
        self.close()

    def __get_md5(self):
        return hashlib.md5(self.url.encode()).hexdigest()

    def __save_url_md5_csv(self):
        row = [self.url, self.md5]
        self.url_md5_csv.open(mode='a')
        self.url_md5_csv.writerow(row)
        self.url_md5_csv.close()

    def __set_driver(self):
        options = Options()
        if self.config.driver_headless:
            options.add_argument('--headless')
        options.add_argument(f'--window-size={self.config.driver_window_size}')
        self.driver = webdriver.Chrome(self.config.driver_path, options=options)
        return self.driver

    def __get_url(self):
        self.driver.get(self.url)
        return self.driver

    def __save_main_screenshot(self):
        self.driver.save_screenshot(f'bot-facebook_{self.md5}.png')

    def close(self):
        self.driver.close()
        return self.driver


if __name__ == '__main__':
    url1 = 'https://www.facebook.com/profile.php?id=100003563130499'
    url2 = 'https://www.facebook.com/EsenyurtBLDYS'

    cand1 = Facebook(url1)
    cand2 = Facebook(url2)
