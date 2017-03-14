import config
from base_plugin import BasePlugin
from storage import Storage, DatabaseConnection


class DomainsPlugin(BasePlugin):

    def get_config_options(self):
        pass

    def _insert_in_db(data, url):
        pass

    def get_storage(self):
        conf_obj = config.Config("/home/user1/intership/crawler.conf")
        conf = conf_obj.config_options
        connection = DatabaseConnection(conf)
        self.storage = Storage(connection)

    def _store(self):
        domains = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domains.append(domain)
        self._insert_in_db(domains, url)



class DomainComPlugin(DomainsPlugin):

    def get_config_options(self):
        conf = config.Config('/home/user1/intership/domain_com_plugin.conf')
        self.config_options = conf.config_options

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if\
                  self.config_options['options']['available_domain']\
                  in domain]
        if domains:
            self.storage.insert_domains(domains, url)


class RestrictedDomains(DomainsPlugin):

    def get_config_options(self):
        conf = config.Config('/home/user1/intership/restricted_domains.conf')
        self.config_options = conf.config_options

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if domain\
                  in self.config_options['options']['blocked_domains']]
        if domains:
            self.storage.insert_restricted_domains(domains, url)

