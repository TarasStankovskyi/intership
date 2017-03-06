from mysql_storage import MySQLStorage


STORAGE = {'mysql' : MySQLStorage}

def get_storage(storage_type):
    return STORAGE[storage_type]()

