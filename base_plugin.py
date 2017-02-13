from storage import Storage, DatabaseConnection
import config
from netaddr import IPAddress, IPRange



class BasePlugin(object):
    def __init__(self, storage, data):
        self.storage = storage
        self.data = data
        self.conf = config.Config('/home/user1/intership/plugins.conf')
        self.config_options = self.conf.config_options

    def _store(self):
        raise NotImplementedError('You need to implement this method')

    def run(self):
        self._store()


if __name__ == '__main__':
   pass
