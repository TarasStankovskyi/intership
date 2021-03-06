import socket
import config
import storage
from threading import Thread
from collections import defaultdict
from crawler import Crawler


class Server(object):

    def __init__(self, port=8001, que=5):
        self.port = port
        self.que = que
        self.__parse_config()
        self.storage = storage.get_storage(self.config_options['storage']\
                                          ['type'])
        self.plugins = []
        for plugin in self.config_options['active_plugins']:
            module = __import__(plugin)
            self.plugins.append(getattr(module,
                               self.config_options['active_plugins']\
                               [plugin])(self.config_options['paths']\
                               ['plugins_path']))
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

    def __parse_config(self):
        conf_obj = config.Config('/home/user1/intership/server.conf')
        self.config_options = conf_obj.config_options

    def _execute(self, data):
        crawler = Crawler()
        for url in data.split(' '):
            data = crawler.run(url)
            self.storage.insert_url(url)
            for plugin in self.plugins:
                plugin.run(data)


    def _run(self, client_socket, address):
        while True:
            try:
                data = client_socket.recv(1024)
                if data:
                        self._execute(data)
                        client_socket.send('Data has been saved\n')
                else:
                    client_socket.send('Processing...\n')
                    break
            except KeyboardInterrupt:
                client_socket.send('Error occured')
        client_socket.close()

    def shutdown(self):
        self.storage.close()
        self.sock.close()


if  __name__ == '__main__':
    pass
