import socket
from collections import defaultdict
from crawler import Crawler
from storage import Storage, DatabaseConnection
import config

class Server(object):

    def __init__(self, port=8001, que=1):
        self.arguments = []
        self.port = port
        self.que = que

    def __connection(self):
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', self.port))
            sock.listen(self.que)
            client_socket, address = sock.accept()
            print 'Listening from {}'.format(address)
            while True:
                data = client_socket.recv(1024)[:-2]
                if data:
                    self.arguments.append(data)
                else:
                    print 'No more data. Processing ...'
                    break

        finally:
            sock.close()

    def run(self):
        self.__connection()
        conf_object = config.Config("/home/user1/intership/crawler.conf")
        conf = conf_object.config_options
        crawler = Crawler(self.arguments)

        data = crawler.run()
        connection = DatabaseConnection(conf)
        storage = Storage(connection)

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
                storage.insert_ips(ips, domain)
            for domain, mails in domain_mails.items():
                storage.insert_mails(mails, url, domain)
        storage.close()
        print 'Data has been saved'


if  __name__ == '__main__':
    pass
