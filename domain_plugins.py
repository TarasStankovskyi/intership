from base_plugin import BasePlugin



class DomainsPlugin(BasePlugin):

    def _insert_in_db(data, url):
        pass

    def _store(self):
        domains = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                domains.append(domain)
        self._insert_in_db(domains, url)



class DomainComPlugin(DomainsPlugin):
    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if\
                  self.config_options['DomainComPlugin']['available_domain']\
                  in domain]
        if domains:
            self.storage.insert_domains(domains, url)


class RestrictedDomains(DomainsPlugin):

    def _insert_in_db(self, data, url):
        domains = [domain for domain in data if domain\
                  in self.config_options['RestrictedDomains']['blocked_domains']]
        if domains:
            self.storage.insert_restricted_domains(domains, url)

