import argparse
import sqlite3
import webbrowser
import requests


def main():
    opts = parse_options()
    database_test()

    if opts.open:
        resp = requests.get(opts.open)
        if resp.status_code == 200:
            webbrowser.open_new_tab(opts.open)
        else:
            message = 'Connection failed with status code: ' + str(resp.status_code)
            raise requests.ConnectionError(message)


def parse_options():
    parser = argparse.ArgumentParser(description='Create and redirect to shortened URLs')
    parser.add_argument('-o', '--open', help='Open a URL')
    parser.add_argument('-s ', '--shorten', help='Create a shortened URL')
    args = parser.parse_args()

    if args.open and args.shorten:
        message = 'The arguments "open" and "shorten" cannot be used together'
        raise Exception(message)

    return args


def database_test():
    mydb = sqlite3.connect('../database/url_shortener.db')

    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM urls')
    print(mycursor.fetchone())


if __name__ == '__main__':
    main()
