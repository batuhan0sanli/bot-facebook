import hashlib
from __init__ import url_md5_csv


class Facebook:
    def __init__(self, url):
        self.url = url
        self.md5 = self.__get_md5()
        self.url_md5_csv = url_md5_csv

        # url-md5.csv
        self.__save_url_md5_csv()

    def __get_md5(self):
        return hashlib.md5(self.url.encode()).hexdigest()

    def __save_url_md5_csv(self):
        row = [self.url, self.md5]
        self.url_md5_csv.open(mode='a')
        self.url_md5_csv.writerow(row)
        self.url_md5_csv.close()


if __name__ == '__main__':
    url1 = 'https://www.facebook.com/profile.php?id=100003563130499'
    url2 = 'https://www.facebook.com/EsenyurtBLDYS'

    cand1 = Facebook(url1)
    cand2 = Facebook(url2)
