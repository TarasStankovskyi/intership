import config
from base_plugin import BasePlugin


class DomainsPlugin(BasePlugin):

    def _store(self):
        domains = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domains.append(domain)
        self._insert_in_db(domains, url)


if __name__ == '__main__':
    a = DomainComPlugin('/home/user1/intership/plugins/')
    a.run({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2'],
           ['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2']]})
