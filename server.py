import socket
from threading import Thread
from collections import defaultdict
from crawler import Crawler


class Server(object):

    def __init__(self, db_storage, plugins_config, port=8001, que=5):
        self.port = port
        self.que = que
        self.storage = db_storage
        self.plugins_config = plugins_config


    def connect(self):
        while True:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.sock.bind(('', self.port))
            self.sock.listen(self.que)
            while True:
                client_socket, address = self.sock.accept()
                print 'Listening from {}'.format(address)
                Thread(target=self._run, args=(client_socket, address)).start()

    def execute_plugins(self, data):
        module = __import__(self.plugins_config['modules']['module'])
        active_plugins = [plugin for plugin in self.plugins_config['plugins']\
                         if self.plugins_config['plugins'][plugin]]
        for plugin in active_plugins:
            Plugin_Class = getattr(module, plugin)
            Plugin_Class(self.storage).run(data)


    def _execute(self, data):
        crawler = Crawler()
        for url in data.split(' '):
            data = crawler.run(url)
            self.storage.insert_url(url)
            self.execute_plugins(data)

    def _run(self, client_socket, address):
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                        self._execute(data)
                        client_socket.send('Data has been saved')
                else:
                    client_socket.send('Processing...\n')
                    break
            except KeyboardInterrupt:
                client_socket.send('Error occured')
        client_socket.close()

    def shutdown(self):
        self.sock.close()


if  __name__ == '__main__':
    pass
