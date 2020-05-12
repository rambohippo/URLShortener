import argparse
import os
import random
import requests
import string
import sqlite3
import webbrowser
from urllib.parse import urlparse

db_dir = 'database'
db_path = db_dir + '/url_shortener.db'
db_table = 'urls'


def main():
    try:
        opts = parse_options()
        db_initialize()

        if opts.open:
            open_url(opts.open)

        if opts.shorten:
            shorten_url(opts.shorten)

    except KeyboardInterrupt:
        print('Keyboard Interrupt. Quitting.')
        quit(2)
    except Exception as e:
        print(e)
        quit(1)


def parse_options():
    parser = argparse.ArgumentParser(description='Create and redirect to shortened URLs')
    parser.add_argument('-o', '--open', help='Open a URL')
    parser.add_argument('-s', '--shorten', help='Create a shortened URL')
    args = parser.parse_args()

    if args.open and args.shorten:
        message = 'The arguments "--open" and "--shorten" cannot be used together'
        raise RuntimeError(message)

    return args


def open_url(url):
    if db_check_if_exists(url, col='short_url'):
        base_url = db_get_base_url(url)
        print('The input url {} exists in the database as the shortened url of {}'.format(
            url, base_url))
        print('Opening the full url:', base_url)
        url = base_url
    else:
        print('The input url {} does not exist as a shortened version in the database'.format(url))
        print('Opening as normal')

    try:
        resp = requests.get(url)
    except requests.exceptions.MissingSchema as error:
        print('The schema for the given url is incorrect or missing.')
        raise
    except requests.exceptions.ConnectionError as error:
        print('Failed to establish connection to the url', url)
        raise

    if resp.status_code == 200:
        webbrowser.open_new_tab(url)
        print('Successfully opened the web default browser to', url)
    else:
        message = 'Connection to "{}" failed with status code: {}'.format(url, resp.status_code)
        raise RuntimeError(message)


def shorten_url(url):
    if db_check_if_exists(url, col='base_url'):
        message = 'The url {} already has a shortened version in the database'.format(url)
        raise RuntimeError(message)

    parsed_url = urlparse(url)
    if not parsed_url.path:
        message = 'The url {} does not have a path. It cannot be shortened.'.format(url)
        raise RuntimeError(message)

    short_path = '/' + generate_random_string()
    short_url = parsed_url.scheme + '://' + parsed_url.netloc + short_path

    db_insert(parsed_url.geturl(), parsed_url.scheme, parsed_url.netloc,
              parsed_url.path, short_url, short_path)


def generate_random_string(size=10):
    chars = string.ascii_lowercase
    return ''.join(random.choice(chars) for _ in range(size))


def db_insert(base_url, base_protocol, base_domain, base_path,
              short_url, short_path):
    command = "INSERT INTO {} (base_url, base_protocol, base_domain, base_path, short_url, " \
            + "short_path) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')"
    command = command.format(db_table, base_url, base_protocol, base_domain, base_path,
                             short_url, short_path)

    try:
        con = sqlite3.connect(db_path)
        con.execute(command)
        print('Executed the command: ' + command)
        con.commit()
        print('The url "{}" has been shortened to "{}"'.format(base_url, short_url))
    except sqlite3.Error as error:
        print('Error while executing INSERT command:', error)
        raise
    finally:
        if con:
            con.close()


def db_select(cols='*', table=db_table, where=''):
    command = 'SELECT {} FROM {}'.format(cols, table)
    if where:
        command += ' WHERE ' + where

    try:
        con = sqlite3.connect(db_path)
        cursor = con.cursor()
        cursor.execute(command)
        print('Executed the command: ' + command)
        record = cursor.fetchall()
    except sqlite3.Error as error:
        print('Error while executing SELECT command:', error)
        return None
    finally:
        if cursor:
            cursor.close()
        if con:
            con.close()

    return record


def db_check_if_exists(url, col='base_url'):
    condition = col + "='" + url + "'"
    record = db_select(where=condition)
    return len(record) > 0


def db_get_base_url(short_url):
    condition = "short_url='" + short_url + "'"
    record = db_select(cols='base_url', where=condition)
    if len(record) > 0:
        return record[0][0]
    else:
        return ''


def db_initialize():
    # Create database directory if it does not exist
    if not os.path.exists(db_dir):
        os.makedirs(db_dir)

    # Initialize database table if it does not exist
    try:
        command = 'CREATE TABLE IF NOT EXISTS {} (base_url text, base_protocol text, ' \
                + 'base_domain text, base_path text, short_url text, short_path text)'
        command = command.format(db_table)
        con = sqlite3.connect(db_path)
        con.execute(command)
        print('Executed the CREATE TABLE command:', command)
    except sqlite3.Error as error:
        print('Error while initializing database')
        raise
    finally:
        if con:
            con.close()


if __name__ == '__main__':
    main()
