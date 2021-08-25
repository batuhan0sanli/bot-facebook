from save_csv import Csv

# url-md5.csv
fieldnames = ['URL', 'MD5']
url_md5_csv = Csv('url-md5.csv', fieldnames=fieldnames)
url_md5_csv.initialize(close_file=True)