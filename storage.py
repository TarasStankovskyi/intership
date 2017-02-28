import MySQLdb
from collections import Counter

class DatabaseConnection(object):
    def __init__(self, config):
        self.__config = config
        self._db = MySQLdb.connect(self.__config['database']['host'],
                                   self.__config['database']['user'],
                                   self.__config['database']['passwd'],
                                   self.__config['database']['db'],
                                   int(self.__config['database']['port']))
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
            for domain in Counter(domains):
                cursor.execute(
                               """INSERT INTO domains (domain,
                               counter, url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [domain, Counter(domain)[domain], url,
                                     Counter(domain)[domain]])


    def insert_restricted_domains(self, domains, url):
        with self.__connection as cursor:
            for domain in Counter(domains):
                cursor.execute(
                               """INSERT INTO blocked_domains (domain,
                               counter, url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [domain, Counter(domains)[domain], url,
                                    Counter(domains)[domain]])

    def insert_integer_ips(self, data, url):
        with self.__connection as cursor:
            results = []
            for domain, ip in Counter(data):
                results.append([domain, ip, Counter(data)[domain, ip]])
            for domain, ip, counter in results:
                cursor.execute(
                               """INSERT INTO integer_ips (ip, domain,
                               counter, url)
                               VALUES (%s, %s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [ip, domain, counter, url, counter])

    def insert_cidr_ips(self, ips, url):
        with self.__connection as cursor:
            for ip in Counter(ips):
                cursor.execute(
                               """INSERT INTO cidr_ips (ip, counter, url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+%s
                               """, [ip, Counter(ips)[ip], url,
                                    Counter(ips)[ip]])


    def insert_filtered_mails(self, mails, url):
        with self.__connection as cursor:
            for mail in Counter(mails):
                cursor.execute(
                               """INSERT INTO filtered_mails (mail, counter,
                               url)
                               VALUES (%s, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [mail, Counter(mails)[mail], url,
                                    Counter(mails)[mail]])

