import config
from domain_plugins import DomainsPlugin


class DomainComPlugin(DomainsPlugin):

    CONF_FILE = 'domain_com_plugin.conf'

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if\
                  domain.endswith(self.config_options['options']\
                  ['available_domain'])]
        if domains:
            self.storage.insert_domains(domains, url)




if __name__ == '__main__':
    a = DomainComPlugin('/home/user1/intership/plugins/')
    a.run({'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'www.youtube.com', '207.241    .224.2'],['http://purl.org/dc/terms/', 'www.yoube.com', '207.241.224.2']]})

