import json
from os import path, makedirs
from shutil import copyfile

DEF_CONFIG_FILE = "./data/config.json"
DEF_CONFIG_TEMPLATE = "./data/config-template.json"


class __Config:
    def __init__(self):
        self.config = {}
        self.read()

    def read(self):
        if not path.exists(DEF_CONFIG_FILE):
            copyfile(DEF_CONFIG_TEMPLATE, DEF_CONFIG_FILE)

        with open(DEF_CONFIG_FILE, "r") as conf_file:
            try:
                json.load(conf_file)
            except json.JSONDecodeError:
                conf_file.close()
                copyfile(DEF_CONFIG_TEMPLATE, DEF_CONFIG_FILE)
            finally:
                with open(DEF_CONFIG_FILE, "r") as conf_file:
                    self.config = json.load(conf_file)

    def save(self):
        with open(DEF_CONFIG_FILE, "w") as conf_file:
            json.dump(self.config, conf_file, indent=4)


__config = __Config()


def get_email_credentials():
    return __config.config["email"]




