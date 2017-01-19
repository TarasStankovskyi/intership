import MySQLdb


class Storage(object):

    def __init__(self, config):
        self.__config = config
        self.__db = MySQLdb.connect(self.__config['database']['host'],
                                    self.__config['database']['user'],
                                    self.__config['database']['passwd'],
                                    self.__config['database']['db'],
                                    int(self.__config['database']['port']))
        self.__cursor = self.__db.cursor()

    def insert_url(self, url):
        self.__cursor.execute(
                              """INSERT INTO url (url, counter)
                              VALUES (%s, 1)
                              ON DUPLICATE KEY
                              UPDATE counter=counter+1""", [url])
        self.__db.commit()
        return  self.__cursor.lastrowid

    def insert_domain(self, domain, url_id):
        self.__cursor.execute(
                              """INSERT INTO domain (domain,
                              counter, url_id)
                              VALUES (%s, 1, %s)
                              ON DUPLICATE KEY
                              UPDATE counter=counter+1
                              """, [domain, url_id])
        self.__db.commit()
        return  self.__cursor.lastrowid

    def insert_url_domain(self, url_id, domain_id):
        self.__cursor.execute(
                              """INSERT IGNORE INTO url_domain (url_id,
                              domain_id)
                              VALUES (%s, %s)
                              """, [url_id, domain_id])

        self.__db.commit()
    def insert_mail(self, mail, url_id, domain_id):
        self.__cursor.execute(
                              """INSERT INTO mail (mail,  counter,
                              url_id, domain_id)
                              VALUES (%s, 1, %s, %s)
                              ON DUPLICATE KEY
                              UPDATE counter=counter+1
                              """, [mail, url_id, domain_id])
        self.__db.commit()
        return self.__cursor.lastrowid

    def url_mail(self, url_id, mail_id):
        self.__cursor.execute(
                              """INSERT IGNORE INTO url_mail (url_id,
                              mail_id)
                              VALUES (%s, %s)
                              """, [url_id, mail_id])
        self.__db.commit()

    def insert_ip(self, ip, domain_id):
        self.__cursor.execute(
                              """INSERT INTO ip (ip, counter, domain_id)
                              VALUES (%s, 1, %s)
                              ON DUPLICATE KEY
                              UPDATE counter=counter+1
                              """, [ip, domain_id])
        self.__db.commit()









