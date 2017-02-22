import config
from base_plugin import BasePlugin
from netaddr import IPAddress, IPRange
from storage import Storage, DatabaseConnection

class CidrIp(BasePlugin):

    def get_config_options(self):
        conf = config.Config("/home/user1/intership/cidr_ips.conf")
        print conf
        print conf.config_options
        self.config_options = conf.config_options

    def _insert_in_db(self, data, url):
        ips = []
        acceptable_ips = IPRange(self.config_options['options']['ip1'],\
                                 self.config_options['options']['ip2'])
        for ip in data:
            if IPAddress(ip) in acceptable_ips:
                ips.append(ip)
        self.storage.insert_cidr_ips(ips, url)

    def get_storage(self):
        conf_obj = config.Config("/home/user1/intership/crawler.conf")
        conf = conf_obj.config_options
        connection = DatabaseConnection(conf)
        self.storage = Storage(connection)

    def _store(self):
        ips = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                ips.append(ip)
        self._insert_in_db(ips, url)

if __name__ == '__main__':
    x = CidrIp({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'purl.org', '207.241.224.2'], ['http://purl.org/dc/terms/', 'purl.org', '207.241.224.2']]})
    x.get_config_options()
    print x.config_options
