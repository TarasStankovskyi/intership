import sys
import crawler
import process_result as result
import config


conf = config.Config("/home/user1/intership/crawler.conf").config_options
res = result.Storage(conf)
crawler = crawler.Crawler(sys.argv[1:]).run()
for key, value in crawler.items():
    url_id = res.insert_url(key)
    for val in value:
        domain_id = res.insert_domain(val[1], url_id)
        res.insert_url_domain(url_id, domain_id)
        if val[0].startswith('mailto'):
            mail_id = res.insert_mail(val[0], url_id, domain_id)
            res.url_mail(url_id, mail_id)
        res.insert_ip(val[2], domain_id)

