import json
from lynxlms_server.lmsdb import db
from os import path, makedirs
from shutil import copyfile
from lynxlms_server.managers import *

DEF_DB_FILE = "./data/lms_db.db"
DEF_CONFIG_FILE = "./data/config.json"
__DEF_CONFIG_TEMPLATE = "./data/config-template.json"


def drop_tables():
    db.drop_tables(tables, safe=True)


def create_tables():
    db.create_tables(tables, safe=True)


def init_db(db_filename=DEF_DB_FILE):
    dir_name, _ = path.split(db_filename)
    if dir_name != "" and not path.exists(dir_name):
        makedirs(dir_name)
    db.init(db_filename)
    db.connect()


def read_config():
    if not path.exists(DEF_CONFIG_FILE):
        copyfile(__DEF_CONFIG_TEMPLATE, DEF_CONFIG_FILE)

    with open(DEF_CONFIG_FILE, "r") as conf_file:
        try:
            json.load(conf_file)
        except json.JSONDecodeError:
            conf_file.close()
            copyfile(__DEF_CONFIG_TEMPLATE, DEF_CONFIG_FILE)
        finally:
            with open(DEF_CONFIG_FILE, "r") as conf_file:
                config = json.load(conf_file)

    return config


def save_config(config):
    with open(DEF_CONFIG_FILE, "w") as conf_file:
        json.dump(config, conf_file, indent=4)


def prepare(config):
    init_db()
    drop_tables()
    create_tables()
    for doc_type in config["def_doc_types"]:
        fields = json.dumps(config["def_doc_types"][doc_type])
        doc_type_entry = DocType.create(ame=doc_type, fields=fields)
        doc_type_entry.save()

    for group in config["def_groups"]:
        rules = json.dumps(config["def_groups"][group])
        group_entry = Group.create(name=group, rules=rules)
        group_entry.save()


def init_main():
    config = read_config()
    if config["first_run"]:
        prepare(config)
        # config["first_run"] = False
        save_config(config)




