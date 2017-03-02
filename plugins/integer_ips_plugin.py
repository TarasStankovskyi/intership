import config
import storage
from base_plugin import BasePlugin
from netaddr import IPAddress


class IntegerIpsPlugin(BasePlugin):

    CONF_FILE = "integer_ips.conf"

    def _insert_in_db(self, data, url):
        processed_data = []
        for domain, ip in data:
            processed_data.append((domain, int(IPAddress(ip))))
        self.storage.insert_integer_ips(processed_data, url)

    def _store(self):
        domain_ips = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domain_ips.append([domain, ip])
        self._insert_in_db(domain_ips, url)


if __name__ == '__main__':
    a = IntegerIpsPlugin('/home/user1/intership/plugins/', 'mysql', "/home/user1/intership/crawler.conf")
    a.run({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2'],
           ['http://purl.org/dc/terms/', 'www.yoube.com', '207.241.224.2']]})

