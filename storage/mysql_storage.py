import os
import MySQLdb
import config
from collections import Counter


class DatabaseConnection(object):
    def __init__(self, config):
        self.__config = config
        self._db = MySQLdb.connect(self.__config['mysql']['host'],
                                   self.__config['mysql']['user'],
                                   self.__config['mysql']['passwd'],
                                   self.__config['mysql']['db'],
                                   int(self.__config['mysql']['port']))
    def close(self):
        self._db.close()

    def __enter__(self):
        self.__cursor = self._db.cursor()
        return self.__cursor

    def __exit__(self, ext_type, exc_value, traceback):
        if isinstance(exc_value, Exception):
            self._db.rollback()
        else:
            self._db.commit()


class Storage(object):

    def __init__(self, connection):
        self.__connection = connection

    def close(self):
        self.__connection.close()


    def insert_url(self, url):
        with self.__connection as cursor:
            cursor.execute(
                           """INSERT INTO urls (url, counter)
                           VALUES (%s, 1)
                           ON DUPLICATE KEY
                           UPDATE counter=counter+1""", [url])

    def insert_domains(self, domains, url):
        with self.__connection as cursor:
            for domain, counter in Counter(domains).items():
                cursor.execute(
                               """INSERT INTO domains (domain,
                               counter, url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [domain, counter, url,
                                     counter])


    def insert_restricted_domains(self, domains, url):
        with self.__connection as cursor:
            for domain, counter in Counter(domains).items():
                cursor.execute(
                               """INSERT INTO blocked_domains (domain,
                               counter, url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [domain, counter, url,
                                    counter])

    def insert_integer_ips(self, data, url):
        with self.__connection as cursor:
            for data, counter in Counter(data).items():
                cursor.execute(
                               """INSERT INTO integer_ips (ip, domain,
                               counter, url)
                               VALUES (%s, %s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [data[1], data[0], counter, url, counter])

    def insert_cidr_ips(self, ips, url):
        with self.__connection as cursor:
            for ip, counter in Counter(ips).items():
                cursor.execute(
                               """INSERT INTO cidr_ips (ip, counter, url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [ip, counter, url,
                                    counter])


    def insert_filtered_mails(self, mails, url):
        with self.__connection as cursor:
            for mail, counter in Counter(mails).items():
                cursor.execute(
                               """INSERT INTO filtered_mails (mail, counter,
                               url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [mail, counter, url,
                                    counter])


class MySQLStorage(Storage):

    def __init__(self):
        self.CONF_FILE = 'db.conf' 
        self.conf_obj = config.Config(os.environ['CONFROOT'] + self.CONF_FILE)
        self.conf = self.conf_obj.config_options
        self.conn = DatabaseConnection(self.conf)
        super(MySQLStorage, self).__init__(self.conn)
        self.storage = Storage(self.conn)



if __name__ == '__main__':
    s = MySQLStorage()
    print dir(s)
