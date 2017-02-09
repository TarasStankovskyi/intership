import MySQLdb

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
                           """INSERT INTO url (url, counter)
                           VALUES (%s, 1)
                           ON DUPLICATE KEY
                           UPDATE counter=counter+1""", [url])

    def insert_domains(self, domains, url):
        with self.__connection as cursor:
            for domain in domains:
                cursor.execute(
                               """INSERT INTO domain (domain,
                               counter, url)
                               VALUES (%s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [domain, url])


    def insert_restricted_domains(self, domains, url):
        with self.__connection as cursor:
            for domain in domains:
                cursor.execute(
                               """INSERT INTO blocked_domain (domain,
                               counter, url)
                               VALUES (%s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [domain, url])

    def insert_integer_ips(self, data, url):
        with self.__connection as cursor:
            for domain, ip in data:
                cursor.execute(
                               """INSERT INTO integer_ip (ip, domain,
                               counter, url)
                               VALUES (%s, %s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [ip, domain, url])

    def insert_cidr_ips(self, ips, url):
        with self.__connection as cursor:
            for ip in ips:
                cursor.execute(
                               """INSERT INTO cidr_ips (ip, counter, url)
                               VALUES (%s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [ip, url])


    def insert_filtered_mails(self, mails, url):
        with self.__connection as cursor:
            for mail in mails:
                cursor.execute(
                               """INSERT INTO filtered_mails (mail, counter,
                               url)
                               VALUES (%s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [mail, url])

