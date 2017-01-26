from server import Server
import config
from storage import Storage, DatabaseConnection

if __name__ == '__main__':

    server = Server(config.Config("/home/user1/intership/crawler.conf"),
                    DatabaseConnection,
                    Storage)
    conn = server.connect()
