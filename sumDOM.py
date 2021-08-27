import os
from save_csv import Csv
import csv


def giveCsv(folder_name):
    folder_name = './' + folder_name
    return [csv_file for csv_file in os.listdir(folder_name) if csv_file.endswith('.csv')]


def giveMd5(csv_name):
    return csv_name.split('.')[0].split('_')[1]


def giveCsvPath(csv_name, folder_name):
    return f'./{folder_name}/{csv_name}'


def giveDOM(csv_path):
    with open(csv_path) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        next(csv_reader)
        like = 0
        comment = 0
        share = 0
        for row in csv_reader:
            i_like, i_comment, i_share = list(map(int, row))
            like += i_like
            comment += i_comment
            share += i_share
        return [like, comment, share]


if __name__ == '__main__':
    import argparse

    # ArgParse
    parse = argparse.ArgumentParser()
    parse.add_argument('--dir', required=True,)
    args = parse.parse_args()

    MY_DIR = args.dir
    csv_files = giveCsv(MY_DIR)

    fieldnames = ['URL_MD5', 'Begeni', 'Yorum', 'Paylasim']
    sum_csv = Csv(f'./{MY_DIR}/bot-facebook_sum.csv', fieldnames=fieldnames)
    sum_csv.initialize(close_file=True)
    sum_csv.open(mode='a')

    for csv_file in csv_files:
        path = giveCsvPath(csv_file, MY_DIR)
        md5 = giveMd5(csv_file)
        DOMs = giveDOM(path)

        row = [md5] + DOMs
        sum_csv.writerow(row)
    sum_csv.close()

