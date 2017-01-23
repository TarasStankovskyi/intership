import MySQLdb


class Storage(object):

    def __init__(self, cursor):
        self.__cursor = cursor

    def insert_url(self, url):
        self.__cursor.execute(
                              """INSERT INTO url (url, counter)
                              VALUES (%s, 1)
                              ON DUPLICATE KEY
                              UPDATE counter=counter+1""", [url])

    def insert_domains(self, domains, url):
        result = []
        for domain in domains:
            self.__cursor.execute(
                                  """INSERT INTO domain (domain,
                                  counter, url)
                                  VALUES (%s, 1, %s)
                                  ON DUPLICATE KEY
                                  UPDATE counter=counter+1
                                  """, [domain, url])
            result.append((url, domain))
        self.__insert_url_domain(result)


    def __insert_url_domain(self, data):
        self.__cursor.executemany(
                                  """INSERT IGNORE INTO url_domain (url,
                                  domain)
                                  VALUES (%s, %s)
                                  """, data)


    def insert_mails(self, mails, url, domain):
        result = []
        for mail in mails:
            self.__cursor.execute(
                                  """INSERT INTO mail (mail,  counter,
                                  url, domain)
                                  VALUES (%s, 1, %s, %s)
                                  ON DUPLICATE KEY
                                  UPDATE counter=counter+1
                                  """, [mail, url, domain])
            result.append((url, mail))
        self.__insert_url_mail(result)


    def __insert_url_mail(self, data):
        self.__cursor.executemany(
                                  """INSERT IGNORE INTO url_mail (url, mail)
                                  VALUES (%s, %s)
                                  """, data)


    def insert_ips(self, ips, domain):
        for ip in ips:
            self.__cursor.execute(
                                  """INSERT INTO ip (ip, counter, domain)
                                  VALUES (%s, 1, %s)
                                  ON DUPLICATE KEY
                                  UPDATE counter=counter+1
                                  """, [ip, domain])

