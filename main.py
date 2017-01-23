import sys
from collections import defaultdict
from crawler import Crawler
from storage import Storage
from connection import DatabaseConnection
import config



if __name__ == '__main__':
    conf_object = config.Config("/home/user1/intership/crawler.conf")
    config = conf_object.config_options
    crawler = Crawler(sys.argv[1:])
    data = crawler.run()
    with DatabaseConnection(config) as cursor:
        storage = Storage(cursor)

        for url, data in data.items():
            storage.insert_url(url)
            domain_ips = defaultdict(set)
            domain_mails = defaultdict(set)
            domains = []

            for link, domain, ip in data:
                domains.append(domain)
                domain_ips[domain].add(ip)
                if link.startswith('mailto'):
                    domain_mails[domain].add(link.split(':')[1])

            storage.insert_domains(domains, url)
            for domain, ips in domain_ips.items():
                storage.insert_ips(list(ips), domain)
            for domain, mails in domain_mails.items():
                storage.insert_mails(list(mails), url, domain)

