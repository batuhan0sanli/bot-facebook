import argparse
from facebook import Facebook

if __name__ == '__main__':
    parse = argparse.ArgumentParser()
    parse.add_argument('--url', required=True)
    parse.add_argument('--month', required=True)
    args = parse.parse_args()

    url = args.url

    if url.startswith('http'):
        cand = Facebook(url)
        cand.get_month_posts(args.month)
        cand.close()
    else:
        with open(url) as url_list:
            for url in url_list.read().split():
                cand = Facebook(url)
                cand.get_month_posts(args.month)
                cand.close()
