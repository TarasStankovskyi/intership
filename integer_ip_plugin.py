from base_plugin import BasePlugin
from netaddr import IPAddress

class IntegerIpsPlugin(BasePlugin):

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
