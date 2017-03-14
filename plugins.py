from storage import Storage, DatabaseConnection
import config
from netaddr import *



class BasePlugin(object):
    def __init__(self, storage):
        self.storage = storage


    def _insert_in_db(self):
        pass

    def run(self, data):
        raise NotImplementedError('You need to implement this method')


class DomainsPlugin(BasePlugin):

    def _insert_in_db(self, domains, url):
        pass

    def run(self, data):
        domains = []
        for url, data in data.items():
            for link, domain, ip in data:
                domains.append(domain)
        self._insert_in_db(domains, url)


class DomainComPlugin(DomainsPlugin):

    def _insert_in_db(self, domains, url):
        filtered_domains = [domain for domain in domains if '.com' in domain]
        if filtered_domains:
            self.storage.insert_domains(filtered_domains, url)


class RestrictedDomains(DomainsPlugin):

    def _insert_in_db(self, domains, url):
        blocked_domains = ['www.stackoverflow.com', 'www.isport.ua', 'www.vk.com', 'www.youtube.com']
        filtered_domains = [domain for domain in domains\
                   if domain in blocked_domains]
        if filtered_domains:
            self.storage.insert_restricted_domains(filtered_domains, url)


class IntegerIpsPlugin(BasePlugin):

    def _insert_in_db(self, data, url):
        processed_data = []
        for domain, ip in data:
            processed_data.append((domain, int(IPAddress(ip))))
        self.storage.insert_integer_ips(processed_data, url)

    def run(self, data):
        domain_ips = []
        for url, data in data.items():
            for link, domain, ip in data:
                domain_ips.append([domain, ip])
        self._insert_in_db(domain_ips, url)




class CidrIp(BasePlugin):

    def _insert_in_db(self, data, url):
        ips = []
        acceptable_ips = IPRange('212.58.246.0', '212.58.246.255')
        for ip in data:
            if IPAddress(ip) in acceptable_ips:
                ips.append(ip)
        self.storage.insert_cidr_ips(ips, url)


    def run(self, data):
        ips = []
        for url, data in data.items():
            for link, domain, ip in data:
                ips.append(ip)
        self._insert_in_db(ips, url)

class RestrictedMails(BasePlugin):

    def _insert_in_db(self, data, url):
        restricted_mails = ['mail.ru', 'yandex.ru']
        filtered_mails = []
        for mail in data:
            if mail.split('@')[1] not in restricted_mails:
                filtered_mails.append(mail)
        self.storage.insert_filtered_mails(filtered_mails, url)

    def run(self, data):
        mails = []
        for url, data in data.items():
            for link, domain, ip in data:
                if link.startswith('mailto'):
                    mails.append(link.split(':')[1])
        self._insert_in_db(mails, url)

if __name__ == '__main__':
    conf_obj = config.Config("/home/user1/intership/crawler.conf")
    config = conf_obj.config_options
    connection = DatabaseConnection(config)
    db_storage = Storage(connection)
    data = {'http://www.bbc.com/news\r\n': [['http://purl.org/dc/terms/', 'purl.com', '207.241.224.2'], ['http://purl.org/dc/terms/', 'purl.org.com', '207.241.224.2'], ['http://www.bbc.co.uk/a-z/', 'www.isport.ua', '212.58.246.95'], ['http://www.bbc.co.uk/terms/', 'www.stackoverflow.com', '212.58.244.71'], ['https://ssl.bbc.co.uk/favicon.ico', 'www.vk.com', '212.58.246.212'],  ['https://ssl.bbc.co.uk/id/signout', 'ssl.bbc.co.uk', '212.58.244.114'], ['http://www.bbc.co.uk/news/', 'www.bbc.co.uk', '212.58.246.95'], ['http://www.bbc.co.uk/sport/', 'www.bbc.co.uk', '212.58.244.71'], ['http://www.bbc.co.uk/weather/', 'www.bbc.co.uk', '212.58.246.95'], ['http://www.bbc.co.uk/iplayer/', 'www.bbc.co.uk', '212.58.244.71'], ['http://www.bbc.co.uk/tv/', 'www.bbc.co.uk', '212.58.246.95'], ['http://www.bbc.co.uk/radio/', 'www.bbc.co.uk', '212.58.244.71'], ['http://www.bbc.co.uk/cbbc/', 'www.bbc.co.uk', '212.58.246.95'], ['http://www.bbc.co.uk/cbeebies/', 'www.bbc.co.uk', '212.58.244.71'], ['http://www.bbc.co.uk/comedy/', 'www.bbc.co.uk', '212.58.246.95'], ['mailto:bogus@email.com?subject=test', 'email.com', '141.8.224.143'], ['mailto:bogus@email.com?subject=test', 'yandex.ru', '141.8.224.143'] ]}
    x = RestrictedMails(db_storage)
    x.storage.insert_url('http://www.bbc.com/news\r\n')
    x.run(data)
