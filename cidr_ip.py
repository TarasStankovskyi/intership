from base_plugin import BasePlugin
from netaddr import IPAddress, IPRange


class CidrIp(BasePlugin):

    def _insert_in_db(self, data, url):
        ips = []
        acceptable_ips = IPRange(self.config_options['CidrIp']['ip1'],\
                                 self.config_options['CidrIp']['ip2'])
        for ip in data:
            if IPAddress(ip) in acceptable_ips:
                ips.append(ip)
        self.storage.insert_cidr_ips(ips, url)

    def _store(self):
        ips = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                ips.append(ip)
        self._insert_in_db(ips, url)
