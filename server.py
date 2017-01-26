import socket
from collections import defaultdict
from crawler import Crawler

class Server(object):

    def __init__(self, db_storage, port=8001, que=5):
        self.port = port
        self.que = que
        self.storage = db_storage

    def connect(self):
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.bind(('', self.port))
            self.sock.listen(self.que)
            client_socket, address = self.sock.accept()

            print 'Listening from {}'.format(address)

            while True:
                data = client_socket.recv(1024)[:-2]
                if data:
                    for url in data.split(' '):
                        self._run(url)
                else:
                    client_socket.sendall('Processing...\n')
                    print 'No more data. Processing ...'
                    break

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

    def close_connection(self):
        self.sock.close()


if  __name__ == '__main__':
    pass
