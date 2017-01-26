import socket

class Server(object):

    def __init__(self, port=8001, que=1):
        self.arguments = []
        self.port = port
        self.que = que

    def connection(self):
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


if  __name__ == '__main__':
    pass
