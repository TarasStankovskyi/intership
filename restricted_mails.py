import config
from base_plugin import BasePlugin
from storage import DatabaseConnection, Storage


class RestrictedMails(BasePlugin):

    def get_config_options(self):
        conf = config.Config("/home/user1/intership/restricted_mails.conf")
        self.config_options = conf.config_options


    def _insert_in_db(self, data, url):
        filtered_mails = []
        for mail in data:
            if mail.split('@')[1] not in\
                    self.config_options['options']['restricted_mails']:
                        filtered_mails.append(mail)
        self.storage.insert_filtered_mails(filtered_mails, url)


    def get_storage(self):
        conf_obj = config.Config("/home/user1/intership/crawler.conf")
        conf = conf_obj.config_options
        connection = DatabaseConnection(conf)
        self.storage = Storage(connection)

    def _store(self):
        mails = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                if link.startswith('mailto'):
                    mails.append(link.split(':')[1])
        self._insert_in_db(mails, url)

