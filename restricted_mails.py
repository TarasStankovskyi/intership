from base_plugin import BasePlugin



class RestrictedMails(BasePlugin):

    def _insert_in_db(self, data, url):
        filtered_mails = []
        for mail in data:
            if mail.split('@')[1] not in\
                    self.config_options['RestrictedMails']['restricted_mails']:
                        filtered_mails.append(mail)
        self.storage.insert_filtered_mails(filtered_mails, url)

    def _store(self):
        mails = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                if link.startswith('mailto'):
                    mails.append(link.split(':')[1])
        self._insert_in_db(mails, url)
