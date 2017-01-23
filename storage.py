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

    def __iter__(self):
        for item in self.__cursor:
            yield item

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
            result = []
            for domain in domains:
                cursor.execute(
                               """INSERT INTO domain (domain,
                               counter, url)
                               VALUES (%s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [domain, url])
                result.append((url, domain))
            self.__insert_url_domain(result)


    def __insert_url_domain(self, data):
        with self.__connection as cursor:
            cursor.executemany(
                               """INSERT IGNORE INTO url_domain (url,
                               domain)
                               VALUES (%s, %s)
                               """, data)


    def insert_mails(self, mails, url, domain):
        with self.__connection as cursor:
            result = []
            for mail in mails:
                cursor.execute(
                               """INSERT INTO mail (mail,  counter,
                               url, domain)
                               VALUES (%s, 1, %s, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [mail, url, domain])
                result.append((url, mail))
            self.__insert_url_mail(result)


    def __insert_url_mail(self, data):
        with self.__connection as cursor:
            cursor.executemany(
                               """INSERT IGNORE INTO url_mail (url, mail)
                               VALUES (%s, %s)
                               """, data)


    def insert_ips(self, ips, domain):
        with self.__connection as cursor:
            for ip in ips:
                cursor.execute(
                               """INSERT INTO ip (ip, counter, domain)
                               VALUES (%s, 1, %s)
                               ON DUPLICATE KEY
                               UPDATE counter=counter+1
                               """, [ip, domain])

