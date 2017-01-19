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
        try:
            self.__cursor.execute(
                                  """INSERT INTO url (url, counter)
                                  VALUES (%s, 1)
                                  ON DUPLICATE KEY
                                  UPDATE counter=counter+1""", [url])
            self.__db.commit()
        except:
            self.__db.rollback()

    def insert_domains(self, domains, url):
        for domain in domains:
            try:
                self.__cursor.execute(
                                       """INSERT INTO domain (domain,
                                       counter, url)
                                       VALUES (%s, 1, %s)
                                       ON DUPLICATE KEY
                                       UPDATE counter=counter+1
                                       """, [domain, url])
                self.__db.commit()
                self.__insert_url_domain(url, domain)
            except:
                self.__db.rollback()

    def __insert_url_domain(self, url, domain):
        try:
            self.__cursor.execute(
                                  """INSERT IGNORE INTO url_domain (url,
                                  domain)
                                  VALUES (%s, %s)
                                  """, [url, domain])
            self.__db.commit()
        except:
            self.__db.rollback()
    def insert_mails(self, mails, url, domain):
        for mail in mails:
            try:
                self.__cursor.execute(
                                      """INSERT INTO mail (mail,  counter,
                                      url, domain)
                                      VALUES (%s, 1, %s, %s)
                                      ON DUPLICATE KEY
                                      UPDATE counter=counter+1
                                      """, [mail, url, domain])
                self.__db.commit()
                self.__insert_url_mail(url, mail)
            except:
                self.__db.rollback()

    def __insert_url_mail(self, url, mail):
        try:
            self.__cursor.execute(
                                  """INSERT IGNORE INTO url_mail (url,
                                  mail)
                                  VALUES (%s, %s)
                                  """, [url, mail])
            self.__db.commit()
        except:
            self.__db.rollback()

    def insert_ips(self, ips, domain):
        for ip in ips:
            try:
                self.__cursor.execute(
                                      """INSERT INTO ip (ip, counter, domain)
                                      VALUES (%s, 1, %s)
                                      ON DUPLICATE KEY
                                      UPDATE counter=counter+1
                                      """, [ip, domain])
                self.__db.commit()
            except:
                self.__db.rollback()








