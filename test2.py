# todo add utilities

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from datetime import datetime
import time


####################
## === DRIVER === ##
####################
options = Options()
options.add_argument('--headless')
driver = webdriver.Chrome('./chromedriver', options=options)


#######################
## === FUNCTIONS === ##
#######################
def click_posts():
    posts_button = driver.find_element_by_link_text('Gönderiler')
    posts_button.click()
    time.sleep(5)

def see_more_timeline(old_timeline):
    scroll()
    timeline = timeline_element(old_timeline, wait=True)
    return timeline

def scroll():
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)

def close_popUpLogin(driver, timeout=5):
    # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    try:
        element = WebDriverWait(driver, timeout=timeout).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Şimdi Değil')))
    except TimeoutException:
        scroll()
        element = WebDriverWait(driver, timeout=timeout).until(
            EC.presence_of_element_located((By.LINK_TEXT, 'Şimdi Değil')))
    element.click()

def fullscreen_screenshot():
    set_unlimited_window_size()
    driver.find_element_by_tag_name('body').screenshot('foo_fullscreen.png')

def set_unlimited_window_size():
    S = lambda X: driver.execute_script('return document.body.parentNode.scroll' + X)
    driver.set_window_size(S('Width'), S('Height'))

def timeline_element(driver=driver, wait=False):
    if wait:
        return WebDriverWait(driver, timeout=10).until(
            EC.presence_of_element_located((By.XPATH, "//*[@class='_1xnd']")))
        # return WebDriverWait(driver, timeout=10).until(
        #     EC.presence_of_element_located((By.XPATH, "//*[@id='pagelet_timeline_main_column']")))
    else:
        return driver.find_element_by_xpath("//*[@class='_1xnd']")
        # return driver.find_element_by_xpath("//*[@id='pagelet_timeline_main_column']")

def find_like(soup):
    like = soup.find('span', class_='_81hb')

    if not like is None:
        return like.text
    else:
        like_sentence = soup.find('div', class_='UFILikeSentenceText').text

        # Example
        # text = 'Nevim Bekmezci Kavuncu, Nihal Tek, Eda Öztürk ve 127 diğer kişi bunu beğendi.'

        extra_persons = like_sentence.count(',') + 1  # person1, person2 and others => count(',') + 1

        text = like_sentence.split()
        num = int(text[text.index('ve') + 1])  # After 've' (and) word
        like = num + extra_persons  # Total like
        return like

def find_comment(soup):
    comment = soup.find('a', class_='_3hg- _42ft')
    return comment.text.split()[0] if not comment is None else 0

def find_share(soup):
    share = soup.find('a', class_='_3rwx _42ft')
    return share.text.split()[0] if not share is None else 0

def utime2Ym(utime):
    """
    unix time stamp formatını YYYYmm 'a çevirir.
    :param utime:
    :return:
    """
    ts = int(utime)
    return datetime.utcfromtimestamp(ts).strftime('%Y%m')

def find_date(soup):
    date = soup.find('abbr')
    utime = date['data-utime']
    return utime2Ym(utime)



#######################
## === TEST AREA === ##
#######################

url = 'https://www.facebook.com/EsenyurtBLDYS'
# url = 'https://www.facebook.com/Hülya-Erdem-111751313846537'
driver.get(url)

click_posts()
scroll()
close_popUpLogin(driver)



def find_posts_wDate(posts, desired_date, ID):
    set_unlimited_window_size()
    for post in posts:

        html = post.get_attribute('innerHTML')
        soup = BeautifulSoup(html, 'html.parser')

        date = find_date(soup)
        if desired_date == date and not post.id in posts_list:
            posts_list.add(post.id)
            like = find_like(soup)
            comment = find_comment(soup)
            share = find_share(soup)
            num = "{:04d}".format(ID + 1)
            # print(f"ID: {num}  |  DATE: {date}  |  LIKE: {like}  |  COMMENT: {comment}  |  SHARE: {share}")
            ID += 1
            post.screenshot(f'./OCR/{ID}.png')
    if desired_date != date and ID != 0:
        return True, ID
    else:
        return False, ID


desired_date = "202108"
get_xpath = lambda num: "/" + "/div[@class='_1xnd']" * num + "/div[@class='_4-u2 _4-u8']"


ID = 0
num_of_see_more = 1
posts_list = set()
timeline = timeline_element(driver=driver)
while True:
    print(f"{num_of_see_more}. scroll")
    posts = WebDriverWait(timeline, timeout=10).until(
        EC.presence_of_all_elements_located((By.XPATH, get_xpath(num_of_see_more))))

    isStop, ID = find_posts_wDate(posts, desired_date, ID)
    if isStop: break
    timeline = see_more_timeline(timeline)
    num_of_see_more += 1

fullscreen_screenshot()
driver.close()
