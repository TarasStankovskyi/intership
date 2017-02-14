import ConfigParser


class Config(object):

    def __init__(self, filename):
        self.filename = filename
        self.config_options = {}
        self.__parse_config_options()

    def __parse_config_options(self):
        config = ConfigParser.ConfigParser()
        config.optionxform = str
        config.read(self.filename)
        for section in config.sections():
            self.config_options[section] = {}
            for option in config.options(section):
                self.config_options[section][option] = config.get(section, option)





if __name__ == "__main__":
    example = Config("/home/user1/intership/plugins.conf")
    print example.config_options
