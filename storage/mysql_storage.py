import os
import MySQLdb
import config
from collections import Counter


class DBStorage(object):

    CONF_FILE = 'db.conf'

    def __init__(self):
        self.conf_obj = config.Config(os.environ['CONFROOT'] + self.CONF_FILE)
        self._config = self.conf_obj.config_options
        self.connect()

    def close(self):
        self._connection.close()

    def __enter__(self):
        self._cursor = self._connection.cursor()
        return self._cursor

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self._connection.rollback()
        else:
            self._connection.commit()


    def _data_ordering(self, data, url):
        combined_data = [(param, url) for param in data]
        result = []
        for params, counter in Counter(combined_data).items():
            lst = list(params)
            lst.append(counter)
            result.append(lst)
        insert_count = len(result)
        result = [param for params in result for param in params]
        return insert_count, result


    def insert_url(self, urls):
        data = []
        for param in Counter(urls).items():
            data.extend(param)
        query = """INSERT INTO urls (url, counter)
                VALUES""" + ','.join(["(%s, %s)"]*len(urls)) + \
                """ON DUPLICATE KEY
                UPDATE counter=counter+VALUES(counter)"""
        with self._connection as cursor:
            cursor.execute(query, data)

    def insert_domains(self, domains, url):
        insert_count, data = self._data_ordering(domains, url)
        query = """INSERT INTO domains (domain, url, counter)
                VALUES""" + ','.join(["(%s, %s, %s)"]*insert_count) + \
                """ ON DUPLICATE KEY
                UPDATE counter=counter+VALUES(counter)"""
        with self._connection as cursor:
            cursor.execute(query, data)

    def insert_restricted_domains(self, domains, url):
        insert_count, data = self._data_ordering(domains, url)
        query = """INSERT INTO blocked_domains (domain, url, counter)
                VALUES""" + ','.join(["(%s, %s, %s)"]*insert_count) + \
                """ ON DUPLICATE KEY
                UPDATE counter=counter+VALUES(counter)"""
        with self._connection as cursor:
            cursor.execute(query, data)

    def insert_integer_ips(self, data, url):
        combined_data = []
        result = []
        for x in data:
            x.append(url)
            combined_data.append(x)
        combined_data = [tuple(data) for data in combined_data]

        for params, counter in Counter(combined_data).items():
            lst = list(params)
            lst.append(counter)
            result.append(lst)
        insert_count = len(result)
        result = [param for params in result for param in params]
        query = """INSERT INTO integer_ips (domain, ip, url, counter)
                VALUES""" + ','.join(["(%s, %s, %s, %s)"]*insert_count) + \
                """ ON DUPLICATE KEY
                UPDATE counter=counter+VALUES(counter)"""
        with self._connection as cursor:
            cursor.execute(query, result)

    def insert_cidr_ips(self, ips, url):
        insert_count, data = self._data_ordering(ips, url)
        query = """INSERT INTO cidr_ips (ip, url, counter)
                VALUES""" + ','.join(["(%s, %s, %s)"]*insert_count) + \
                """ ON DUPLICATE KEY
                UPDATE counter=counter+VALUES(counter)"""
        with self._connection as cursor:
            cursor.execute(query, data)

    def insert_filtered_mails(self, mails, url):
        insert_count, data = self._data_ordering(mails, url)
        query = """INSERT INTO filtered_mails (mail, url, counter)
                VALUES""" + ','.join(["(%s, %s, %s)"]*insert_count) + \
                """ ON DUPLICATE KEY
                UPDATE counter=counter+VALUES(counter)"""
        with self._connection as cursor:
            cursor.execute(query, data)


class MySQLStorage(DBStorage):

    def connect(self):
        self._connection = MySQLdb.connect(self._config['mysql']['host'],
                                           self._config['mysql']['user'],
                                           self._config['mysql']['passwd'],
                                           self._config['mysql']['db'],
                                           int(self._config['mysql']['port']))


