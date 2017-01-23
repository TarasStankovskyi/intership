import MySQLdb


class DatabaseConnection(object):
    def __init__(self, config):
        self.__config = config
        self._db = MySQLdb.connect(self.__config['database']['host'],
                                   self.__config['database']['user'],
                                   self.__config['database']['passwd'],
                                   self.__config['database']['db'],
                                   int(self.__config['database']['port']))
        self.__cursor = self._db.cursor()

    def __enter__(self):
        return self.__cursor

    def __exit__(self, ext_type, exc_value, traceback):
        self.__cursor.close()
        if isinstance(exc_value, Exception):
            self._db.rollback()
        else:
            self._db.commit()
        self._db.close()

