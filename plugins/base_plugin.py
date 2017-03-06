import config
import storage
from netaddr import IPAddress, IPRange



class BasePlugin(object):

    CONF_FILE = ''

    def __init__(self, plugins_config_path):
        self.get_config_options(plugins_config_path)
        if self.config_options['storage']:
            storage_type = self.config_options['storage']['type']
            self.storage = storage.get_storage(storage_type)

    def _store(self):
        raise NotImplementedError('You need to implement this method')

    def get_config_options(self, plugins_config_path):
        conf = config.Config(plugins_config_path + self.CONF_FILE)
        self.config_options = conf.config_options

    def run(self, data):
        self.data = data
        self._store()


if __name__ == '__main__':
   pass
