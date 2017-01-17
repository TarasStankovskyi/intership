import MySQLdb


class Crawler_Handler(object):

    def __init__(self, config):
        self.__config = config
        self.__db = MySQLdb.connect(self.__config['database']['host'],
                                    self.__config['database']['user'],
                                    self.__config['database']['passwd'],
                                    self.__config['database']['db'],
                                    int(self.__config['database']['port']))
        self.__cursor = self.__db.cursor()

    def write_in_db(self, crawler_result):
        for key, result in crawler_result.items():
            self.__cursor.execute("""START TRANSACTION""")
            self.__cursor.execute(
                                  """INSERT INTO url (url, counter)
                                  VALUES (%s, 1)
                                  ON DUPLICATE KEY
                                  UPDATE counter=counter+1""", [key])
            for res in result:
                self.__cursor.execute(
                                      """INSERT INTO domain (domain,
                                      counter, url_id)
                                      VALUES (%s, 1, (
                                      SELECT url_id FROM url
                                      WHERE url=%s))
                                      ON DUPLICATE KEY
                                      UPDATE counter=counter+1""", [res[1], key])

                self.__cursor.execute(
                                      """INSERT IGNORE INTO url_domain (url_id,
                                      domain_id)
                                      VALUES ((
                                      SELECT url_id FROM url
                                      WHERE url=%s), (
                                      SELECT domain_id FROM domain
                                      WHERE domain=%s))
                                      """, [key, res[1]])

                if res[0].startswith('mailto'):
                    self.__cursor.execute(
                                          """INSERT INTO mail (mail,  counter,
                                          url_id, domain_id)
                                          VALUES (%s, 1, (
                                          SELECT url_id FROM url
                                          WHERE url=%s), (
                                          SELECT domain_id FROM domain
                                          WHERE domain=%s
                                          ))
                                          ON DUPLICATE KEY
                                          UPDATE counter=counter+1
                                          """, [res[0], key, res[1]])

                    self.__cursor.execute(
                                          """INSERT IGNORE INTO url_mail (url_id,
                                          mail_id)
                                          VALUES ((SELECT url_id FROM url
                                          WHERE url=%s), (
                                          SELECT mail_id FROM mail
                                          WHERE mail=%s))
                                          """, [key, res[0]])

                self.__cursor.execute(
                                      """INSERT INTO ip (ip, counter, domain_id)
                                      VALUES (%s, 1, (
                                      SELECT domain_id FROM domain
                                      WHERE domain=%s))
                                      ON DUPLICATE KEY
                                      UPDATE counter=counter+1
                                      """, [res[2], res[1]])


            self.__cursor.execute("""COMMIT""")
            self.__db.commit()








