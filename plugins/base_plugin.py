import config
from storage import Storage, DatabaseConnection
from netaddr import IPAddress, IPRange



class BasePlugin(object):

    def __init__(self, filename, storage_type, config_file):
        self.filename = filename
        self.get_storage(storage_type, config_file)

    def _store(self):
        raise NotImplementedError('You need to implement this method')

    def get_storage(self, storage_type, config_file=None):
        if storage_type == 'mysql':
            conf_obj = config.Config(config_file)
            conf = conf_obj.config_options
            connection = DatabaseConnection(conf)
            self.storage = Storage(connection)

    def get_config_options(self):
        raise NotImplementedError('You need to implement this method')

    def run(self, data):
        self.data = data
        self.get_config_options()
        self._store()


if __name__ == '__main__':
   pass
