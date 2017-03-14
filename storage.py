

STORAGE_TYPE = {'mysql' : 'mysql_storage'}

def get_storage(conf_obj):
    if conf_obj['storage']:
        storage_type = conf_obj['storage']['type']
        module = __import__(STORAGE_TYPE[storage_type])
        return getattr(module, 'storage')()


