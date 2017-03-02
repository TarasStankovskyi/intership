import config
import storage
from base_plugin import BasePlugin


class DomainsPlugin(BasePlugin):

    def _store(self):
        domains = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domains.append(domain)
        self._insert_in_db(domains, url)


class DomainComPlugin(DomainsPlugin):

    CONF_FILE = 'domain_com_plugin.conf'

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if\
                  domain.endswith(self.config_options['options']\
                  ['available_domain'])]
        if domains:
            self.storage.insert_domains(domains, url)


class RestrictedDomains(DomainsPlugin):

    CONF_FILE = 'restricted_domains.conf'

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data for blocked_domain\
                  in self.config_options['options']['blocked_domains'].split(',')\
                  if domain == blocked_domain]
        if domains:
            self.storage.insert_restricted_domains(domains, url)


if __name__ == '__main__':
    a = DomainComPlugin('/home/user1/intership/plugins/')
    a.run({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2'],
           ['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2']]})
