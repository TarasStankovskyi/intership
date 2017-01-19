import sys
import crawler
import process_result as result
import config


conf = config.Config("/home/user1/intership/crawler.conf").config_options
res = result.Storage(conf)
crawler = crawler.Crawler(sys.argv[1:]).run()
domain_ips = {}
for values in crawler.values():
    for val in values:
        domain_ips.setdefault(val[1], [])
        if val[2] not in domain_ips[val[1]]:
            domain_ips[val[1]].append(val[2])


domain_mails = {}
for values in crawler.values():
    for val in values:
        if val[0].startswith('mailto'):
            domain_mails.setdefault(val[1], [])
            if val[0] not in domain_mails[val[1]]:
                domain_mails[val[1]].append(val[0].split(':')[1])

for url, values in crawler.items():
    res.insert_url(url)
    domains = [val[1] for val in values]
    res.insert_domains(domains, url)
    for domain, ips in domain_ips.items():
        res.insert_ips(ips, domain)
    for domain, mails in domain_mails.items():
        res.insert_mails(mails, url, domain)


