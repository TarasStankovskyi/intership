import config
from domain_plugins import DomainsPlugin



class RestrictedDomains(DomainsPlugin):

    CONF_FILE = 'restricted_domains.conf'

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data for blocked_domain\
                  in self.config_options['options']['blocked_domains'].split(',')\
                  if domain == blocked_domain]
        if domains:
            self.storage.insert_restricted_domains(domains, url)

