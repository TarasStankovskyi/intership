import sys
from collections import defaultdict
import crawler
import process_result as result
import config



if __name__ == '__main__':
    conf = config.Config("/home/user1/intership/crawler.conf").config_options
    res = result.Storage(conf)
    crawler = crawler.Crawler(sys.argv[1:]).run()
    domain_ips = defaultdict(set)
    domain_mails = defaultdict(set)
    for values in crawler.values():
        for link, domain, ip in values:
            domain_ips[domain].add(ip)
            if link.startswith('mailto'):
                domain_mails[domain].add(link.split(':')[1])

    for url, values in crawler.items():
        res.insert_url(url)
        domains = [dom[1] for dom in values]
        res.insert_domains(domains, url)
        for domain, ips in domain_ips.items():
            res.insert_ips(list(ips), domain)
        for domain, mails in domain_mails.items():
            res.insert_mails(list(mails), url, domain)

