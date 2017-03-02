import config
import storage
from netaddr import IPAddress, IPRange



class BasePlugin(object):

    CONF_FILE = ''

    def __init__(self, plugins_config_path):
        self.plugins_config_path = plugins_config_path
        self.get_config_options()
        if self.config_options:
            self.storage = storage.get_storage(self.config_options)

    def _store(self):
        raise NotImplementedError('You need to implement this method')

    def get_config_options(self):
        conf = config.Config(self.plugins_config_path + self.CONF_FILE)
        self.config_options = conf.config_options

    def run(self, data):
        self.data = data
        self._store()


if __name__ == '__main__':
   pass
