from mysql_storage import MySQLStorage


STORAGE = {'mysql' : MySQLStorage}

def get_storage(storage_type):
    try:
        return STORAGE.get(storage_type)()
    except TypeError:
        print 'unknown type'
