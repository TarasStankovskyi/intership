import ConfigParser


class Config(object):

    def __init__(self, filename):
        self.filename = filename
        self.__config_options = {}

    def parse_config_options(self):
        config = ConfigParser.ConfigParser()
        config.read(self.filename)
        for section in config.sections():
            self.__config_options[section] = {}
            for option in config.options(section):
                self.__config_options[section][option] = config.get(section, option)
        return self.__config_options




if __name__ == "__main__":
    example = Config("/home/user1/intership/crawler.conf")
    print example.filename
