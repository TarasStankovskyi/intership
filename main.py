import config
from server import Server


if __name__ == '__main__':
    server = Server()
    try:
        conn = server.connect()
    except KeyboardInterrupt:
        server.shutdown()
