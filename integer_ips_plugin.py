import config
from base_plugin import BasePlugin
from netaddr import IPAddress
from storage import DatabaseConnection, Storage


class IntegerIpsPlugin(BasePlugin):

    def get_config_options(self):
        pass

    def _insert_in_db(self, data, url):
        processed_data = []
        for domain, ip in data:
            processed_data.append((domain, int(IPAddress(ip))))
        self.storage.insert_integer_ips(processed_data, url)

    def get_storage(self):
        conf_obj = config.Config("/home/user1/intership/crawler.conf")
        conf = conf_obj.config_options
        connection = DatabaseConnection(conf)
        self.storage = Storage(connection)

    def _store(self):
        domain_ips = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domain_ips.append([domain, ip])
        self._insert_in_db(domain_ips, url)
