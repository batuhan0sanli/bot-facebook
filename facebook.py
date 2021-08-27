import hashlib
from __init__ import url_md5_csv
from config import Config
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from save_csv import Csv
from datetime import datetime
import time


class Facebook:
    def __init__(self, url):
        self.url = url
        self.md5 = self.__get_md5()
        self.url_md5_csv = url_md5_csv
        self.myMonth = None
        self.posts_list = None

        # Config
        self.config = Config()

        # url-md5.csv
        self.__save_url_md5_csv()

        # Selenium
        self.driver = self.__set_driver()
        self.__get_url()
        self.__save_main_screenshot()
        #self.close()

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
        # options.add_argument(f'--window-size={self.config.driver_window_size}')
        self.driver = webdriver.Chrome(self.config.driver_path, options=options)
        return self.driver

    def __get_url(self):
        self.driver.get(self.url)
        return self.driver

    def __set_unlimited_window_size(self):
        S = lambda X: self.driver.execute_script('return document.body.parentNode.scroll' + X)
        self.driver.set_window_size(S('Width'), S('Height'))

    def __save_main_screenshot(self):
        self.driver.save_screenshot(f'bot-facebook_{self.md5}.png')

    def __save_fullscreen_screenshot(self):
        self.__set_unlimited_window_size()
        self.driver.find_element_by_tag_name('body').screenshot(f'bot-facebook_{self.myMonth}_{self.md5}.png')

    def __click_posts(self):
        posts_button = self.driver.find_element_by_link_text(self.config.findElement_clickPosts)
        posts_button.click()
        time.sleep(self.config.driver_sleep_after_action)

    def __scroll(self):
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(self.config.driver_sleep_after_action)

    def __close_popUpLogin(self):
        try:
            element = WebDriverWait(self.driver, timeout=self.config.driver_timeout).until(
                EC.presence_of_element_located((By.LINK_TEXT, self.config.findElement_closePopUpLogin)))
        except TimeoutException:
            self.__scroll()
            element = WebDriverWait(self.driver, timeout=self.config.driver_timeout).until(
                EC.presence_of_element_located((By.LINK_TEXT, self.config.findElement_closePopUpLogin)))
        element.click()

    def __timeline_element(self, driver, wait=False):
        if wait:
            return WebDriverWait(driver, timeout=self.config.driver_timeout).until(
                EC.presence_of_element_located((By.XPATH, self.config.findElement_timeline)))
        else:
            return driver.find_element_by_xpath(self.config.findElement_timeline)

    def __see_more_timeline(self, old_timeline):
        self.__scroll()
        timeline = self.__timeline_element(old_timeline, True)
        return timeline

    def __find_like(self, soup):
        like = soup.find('span', class_='_81hb')

        if not like is None:
            return like.text
        else:
            like_sentence = soup.find('div', class_=self.config.findElement_like).text

            extra_persons = like_sentence.count(',') + 1  # person1, person2 and others => count(',') + 1

            text = like_sentence.split()
            num = int(text[text.index(self.config.findElement_AndWord) + 1])  # After 've' (and) word
            like = num + extra_persons  # Total like
            return like

    def __find_comment(self, soup):
        comment = soup.find('a', class_=self.config.findElement_comment)
        return comment.text.split()[0] if not comment is None else 0

    def __find_share(self, soup):
        share = soup.find('a', class_=self.config.findElement_share)
        return share.text.split()[0] if not share is None else 0

    @staticmethod
    def utime2Ym(utime):
        """ unix time stamp -> YYYYmm """
        ts = int(utime)
        return datetime.utcfromtimestamp(ts).strftime('%Y%m')

    def __find_date(self, soup):
        date = soup.find('abbr')
        utime = date['data-utime']
        return self.utime2Ym(utime)

    def __find_posts_wDate(self, posts, desired_date, ID, dom_csv):
        self.__set_unlimited_window_size()
        for post in posts:

            html = post.get_attribute('innerHTML')
            soup = BeautifulSoup(html, 'html.parser')

            date = self.__find_date(soup)
            if desired_date == date and not post.id in self.posts_list:
                self.posts_list.add(post.id)
                like = self.__find_like(soup)
                comment = self.__find_comment(soup)
                share = self.__find_share(soup)
                num = "{:04d}".format(ID + 1)

                # Save CSV
                row = [like, comment, share]
                dom_csv.writerow(row)

                ID += 1
                post.screenshot(f'./OCR/bot-facebook_{desired_date}_{self.md5}_{num}.png')
        if desired_date != date and ID != 0:
            return True, ID
        else:
            return False, ID

    def get_month_posts(self, desired_date):
        self.posts_list = set()
        self.__click_posts()
        self.__scroll()
        self.__close_popUpLogin()
        self.myMonth = desired_date
        self.__get_xpath = lambda num: "/" + "/div[@class='_1xnd']" * num + "/div[@class='_4-u2 _4-u8']"

        # Csv File
        fieldnames = ['Begeni', 'Yorum', 'Paylasim']
        dom_csv = Csv(f'./DOM/bot-facebook{self.md5}.csv', fieldnames=fieldnames)
        dom_csv.initialize(close_file=True)
        dom_csv.open(mode='a')

        ID = 0
        num_of_see_more = 1
        timeline = self.__timeline_element(driver=self.driver)
        while True:
            print(f"{num_of_see_more}. scroll")
            posts = WebDriverWait(timeline, timeout=self.config.driver_timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, self.__get_xpath(num_of_see_more))))

            isStop, ID = self.__find_posts_wDate(posts, desired_date, ID, dom_csv)
            if isStop: break
            timeline = self.__see_more_timeline(timeline)
            num_of_see_more += 1

        dom_csv.close()
        self.__save_fullscreen_screenshot()


    def close(self):
        self.driver.close()
        return self.driver


if __name__ == '__main__':
    url1 = 'https://www.facebook.com/profile.php?id=100003563130499'
    url2 = 'https://www.facebook.com/EsenyurtBLDYS'

    # cand1 = Facebook(url1)
    # cand1.close()

    cand2 = Facebook(url2)
    cand2.get_month_posts("202108")
    cand2.close()
