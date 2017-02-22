import config
from storage import Storage, DatabaseConnection
from netaddr import IPAddress, IPRange



class BasePlugin(object):

    def _store(self):
        raise NotImplementedError('You need to implement this method')

    def get_storage(self):
        raise NotImplementedError('You need to implement this method')

    def get_config_options(self):
        raise NotImplementedError('You need to implement this method')

    def run(self, data):
        self.data = data
        self.get_config_options()
        self.get_storage()
        self._store()


if __name__ == '__main__':
   pass
