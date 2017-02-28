import os
import config
from base_plugin import BasePlugin
from storage import Storage, DatabaseConnection


class DomainsPlugin(BasePlugin):

    def get_config_options(self):
        pass

    def _insert_in_db(data, url):
        pass

    def _store(self):
        domains = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domains.append(domain)
        self._insert_in_db(domains, url)



class DomainComPlugin(DomainsPlugin):

    def get_config_options(self):
        conf = config.Config(self.filename + 'domain_com_plugin.conf')
        self.config_options = conf.config_options

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if\
                  domain.endswith(self.config_options['options']\
                  ['available_domain'])]
        if domains:
            self.storage.insert_domains(domains, url)


class RestrictedDomains(DomainsPlugin):

    def get_config_options(self):
        conf = config.Config(self.filename + 'restricted_domains.conf')
        self.config_options = conf.config_options


    def _insert_in_db(self, data, url):
        domains = [domain for domain in data for blocked_domain\
                  in self.config_options['options']['blocked_domains'].split(',')\
                  if domain == blocked_domain]
        if domains:
            self.storage.insert_restricted_domains(domains, url)


if __name__ == '__main__':
    a = RestrictedDomains('/home/user1/intership/plugins/', 'mysql', "/home/user1/intership/crawler.conf")
    a.run({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2'],
           ['http://purl.org/dc/terms/', 'www.youtube.com', '207.241.224.2']]})
