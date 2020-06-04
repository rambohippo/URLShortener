import os
import sqlite3
import unittest
import shorten_url

testdb_dir = 'database'
testdb_path = testdb_dir + '/url_shortener.db'
testdb_table = 'urls'


class DatabaseTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create database directory if it does not exist
        if not os.path.exists(testdb_dir):
            os.makedirs(testdb_dir)

        # Initialize database table if it does not exist
        try:
            command = 'CREATE TABLE IF NOT EXISTS {} (base_url text, base_protocol text, ' \
                      + 'base_domain text, base_path text, short_url text, short_path text)'
            command = command.format(testdb_table)
            con = sqlite3.connect(testdb_path)
            con.execute(command)
            print('Executed the CREATE TABLE command:', command)
            print('UnitTest Set Up Completed')
        except sqlite3.Error:
            print('Error while initializing database')
            raise
        finally:
            if con:
                con.close()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(testdb_path)
            os.removedirs(testdb_dir)
            print('UnitTest Tear Down completed')
        except OSError as e:
            print('The file {} could not be removed from the file system'.format(testdb_path))
            print(e)

    def test_db_check_if_exists_empty(self):
        self.assertFalse(shorten_url.db_check_if_exists('https://www.google.com/testsearch'))

    def test_db_check_if_exists_data(self):
        testsite_info = ['https://www.w3schools.com/python/python_mysql_insert.asp',
                         'https', 'www.w3schools.com', '/python/python_mysql_insert.asp',
                         'https://www.w3schools.com/jrvmtxdpyi', '/jrvmtxdpyi']
        shorten_url.db_insert(testsite_info[0], testsite_info[1], testsite_info[2],
                              testsite_info[3], testsite_info[4], testsite_info[5],
                              db_path=testdb_path)
        self.assertTrue(shorten_url.db_check_if_exists(testsite_info[0], db_path=testdb_path))

    def test_db_insert(self):
        testsite_info = ['https://pythonspot.com/python-database-programming-sqlite-tutorial/',
                         'https', 'pythonspot.com', '/python-database-programming-sqlite-tutorial/',
                         'https://pythonspot.com/hwlpgtpudr', '/hwlpgtpudr']
        shorten_url.db_insert(testsite_info[0], testsite_info[1], testsite_info[2],
                              testsite_info[3], testsite_info[4], testsite_info[5],
                              db_path=testdb_path)
        self.assertTrue(shorten_url.db_check_if_exists(testsite_info[0], db_path=testdb_path))

    def test_db_select_base_url(self):
        testsite_info = ['https://pyvideo.org/europython-2014/writing-awesome-command-line-programs-in-python.html',
                         'https', 'pyvideo.org', '/europython-2014/writing-awesome-command-line-programs-in-python.html',
                         'https://pyvideo.org/qfeaoglgpi', '/qfeaoglgpi']
        shorten_url.db_insert(testsite_info[0], testsite_info[1], testsite_info[2],
                              testsite_info[3], testsite_info[4], testsite_info[5],
                              db_path=testdb_path)

        condition = "base_url='" + testsite_info[0] + "'"
        record = shorten_url.db_select(db_path=testdb_path, table=testdb_table, where=condition)

        for aa, bb in zip(testsite_info, record[0]):
            self.assertEquals(aa, bb)

    def test_db_select_short_url(self):
        testsite_info = [
            'https://www.dcrainmaker.com/2020/03/elites-sterzo-steering-riser-block-accessory-in-depth-review.html',
            'https', 'www.dcrainmaker.com',
            '/2020/03/elites-sterzo-steering-riser-block-accessory-in-depth-review.html',
            'https://www.dcrainmaker.com/leqqvzktiw', '/leqqvzktiw']
        shorten_url.db_insert(testsite_info[0], testsite_info[1], testsite_info[2],
                              testsite_info[3], testsite_info[4], testsite_info[5],
                              db_path=testdb_path)

        condition = "short_url='" + testsite_info[4] + "'"
        record = shorten_url.db_select(db_path=testdb_path, table=testdb_table, where=condition)

        for aa, bb in zip(testsite_info, record[0]):
            self.assertEquals(aa, bb)
