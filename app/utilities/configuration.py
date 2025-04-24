import configparser

config_path = "config.ini"

config = configparser.ConfigParser()
config.read(config_path)

APP_CONFIG = config["APP_PROPERTIES"]
