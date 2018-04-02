import json
from os import path, makedirs
from shutil import copyfile
from managers import group_manager

DEF_CONFIG_FILE = "./data/config.json"
DEF_CONFIG_TEMPLATE = "./data/config-template.json"


class __Config:
    def __init__(self):
        self.config = {}
        self.read()
        if self.config["first_run"]:
            self.prepare()
            self.config["first_run"] = False
            self.save()

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

    def prepare(self):
        # Ignore old data
        # for doc_type in self.config["def_doc_types"]:
        #     fields = json.dumps(self.config["def_doc_types"][doc_type]["fields"])
        #     doc_type_entry = DocType.create(name=doc_type, fields=fields)
        #     doc_type_entry.save()
        #
        # for group in self.config["def_groups"]:
        #     group_rules = self.config["def_groups"][group]
        #     group_rules = {DocType.get(DocType.name == k).id: group_rules[k] for k in group_rules}
        #     rules = json.dumps(group_rules)
        #     group_entry = Group.create(name=group, rules=rules)
        #     group_entry.save()
        group_manager.Group.create(name='Students', book_ct=3, book_bestseller_ct=1, journal_ct=2, av_ct=2,
                                            book_rt=3, book_bestseller_rt=1, journal_rt=2, av_rt=2, priority=1)
        group_manager.Group.create(name='Faculty', book_ct=4, book_bestseller_ct=4, journal_ct=2, av_ct=2,
                                            book_rt=4, book_bestseller_rt=4, journal_rt=2, av_rt=2, priority=2)
        group_manager.Group.create(name='Visiting professors', book_ct=4, book_bestseller_ct=4, journal_ct=2, av_ct=2,
                                            book_rt=1, book_bestseller_rt=1, journal_rt=1, av_rt=1, priority=0)


__config = __Config()


def get_email_credentials():
    return __config.config["email"]




