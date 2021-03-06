from base_plugin import BasePlugin


class RestrictedMails(BasePlugin):

    CONF_FILE = "restricted_mails.conf"

    def _insert_in_db(self, data, url):
        filtered_mails = []
        for mail in data:
            if mail.split('@')[1] not in\
                    self.config_options['options']['restricted_mails']:
                        filtered_mails.append(mail)
        if filtered_mails:
            self.storage.insert_filtered_mails(filtered_mails, url)

    def _store(self):
        mails = []
        for url, data in self.data.items():
            for link, domain, ip in data:
                if link.startswith('mailto'):
                    mails.append(link.split(':')[1])
        self._insert_in_db(mails, url)


if __name__ == '__main__':
    a = RestrictedMails('/home/user1/intership/plugins/')
    a.run({'http://www.bbc.com/news\r\n': [['mailto:example@mail.ru', 'www.youtube.com', '207.241.224.2'],['mailto:mail@gmail.com/', 'www.stackoverflow.com', '207.241.224.2']]})
