import socket
from collections import defaultdict
from crawler import Crawler

class Server(object):

    def __init__(self, config, db_connection, db,  port=8001, que=5):
        self.arguments = []
        self.port = port
        self.que = que
        self.conf_object = config
        self.conf = self.conf_object.config_options
        self.db_connection = db_connection(self.conf)
        self.storage = db(self.db_connection)

    def connect(self):
        while True:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.bind(('', self.port))
            sock.listen(self.que)
            client_socket, address = sock.accept()

            print 'Listening from {}'.format(address)

            while True:
                client_socket.sendall("Write down urls : \n")
                data = client_socket.recv(1024)[:-2]
                if data:
                    for url in data.split(' '):
                        self._run(url)
                else:
                    client_socket.sendall('Processing...\n')
                    print 'No more data. Processing ...'
                    continue
            self.storage.close()
            sock.close()

    def _run(self, url):
        crawler = Crawler()
        data = crawler.run(url)

        for url, data in data.items():
            self.storage.insert_url(url)
            domain_ips = defaultdict(set)
            domain_mails = defaultdict(set)
            domains = []

            for link, domain, ip in data:
                domains.append(domain)
                domain_ips[domain].add(ip)
                if link.startswith('mailto'):
                    domain_mails[domain].add(link.split(':')[1])

            self.storage.insert_domains(domains, url)
            for domain, ips in domain_ips.items():
                self.storage.insert_ips(ips, domain)
            for domain, mails in domain_mails.items():
                self.storage.insert_mails(mails, url, domain)
        print 'Data has been saved'


if  __name__ == '__main__':
    pass
