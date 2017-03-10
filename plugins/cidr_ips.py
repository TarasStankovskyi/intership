import config
from base_plugin import BasePlugin
from netaddr import IPAddress, IPRange


class CidrIp(BasePlugin):

    CONF_FILE = "cidr_ips.conf"

    def _insert_in_db(self, data, url):
        alloved_ips = []
        for ip in data:
            for ips in self.config_options['options']['ips'].split(','):
                min_ip, max_ip = ips.split('-')
                acceptable_ips = IPRange(min_ip, max_ip)
                if IPAddress(ip) in acceptable_ips:
                    alloved_ips.append(ip)
        self.storage.insert_cidr_ips(alloved_ips, url)

    def _store(self):
        for url, data in self.data.items():
            ips = []
            for link, domain, ip in data:
                ips.append(ip)
            self._insert_in_db(ips, url)

if __name__ == '__main__':
    x = CidrIp('/home/user1/intership/plugins/')
    x.run({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'www.youtube.com', '212.58.246.2'],
        ['http://purl.org/dc/terms/', 'www.stackoverflow.com', '212.58.246.29']]})

