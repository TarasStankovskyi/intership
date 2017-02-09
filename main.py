from server import Server
import config
from storage import Storage, DatabaseConnection

if __name__ == '__main__':
    conf_obj = config.Config("/home/user1/intership/crawler.conf")
    plugins_config = config.Config('/home/user1/intership/plugins.conf')
    config = conf_obj.config_options
    plugins = plugins_config.config_options
    connection = DatabaseConnection(config)
    db_storage = Storage(connection)
    server = Server(db_storage, plugins)
    try:
        conn = server.connect()
    except KeyboardInterrupt:
        db_storage.close()
        server.shutdown()
