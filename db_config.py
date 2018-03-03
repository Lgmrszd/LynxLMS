import managers.doc_manager
import managers.user_manager
import managers.group_manager
import managers.booking_system
from db_connect import db
from os import path, makedirs


def initialize_db(db_filename="./data/database.db"):
    # Creating tables
    dirname, _ = path.split(db_filename)
    if dirname != "" and not path.exists(dirname):
        makedirs(dirname)
    db.init(db_filename)
    db.connect()
    db.create_tables([managers.doc_manager.Book,
                      managers.doc_manager.AVMaterial,
                      managers.doc_manager.JournalArticle,
                      managers.doc_manager.Copy,
                      managers.user_manager.User,
                      managers.group_manager.Group,
                      managers.booking_system.History], safe=True)
    #deleted_group = managers.group_manager.Group.get(managers.group_manager.Group.name == 'Deleted')
    deleted_group = len(managers.group_manager.Group.select().where(managers.group_manager.Group.name == 'Deleted'))
    if (deleted_group == 0):
        managers.group_manager.Group.create(name='Deleted', book_ct=-1, book_bestseller_ct=-1, journal_ct=-1, av_ct=-1)

def drop_db():
    db.drop_tables([managers.doc_manager.Book,
                    managers.doc_manager.AVMaterial,
                    managers.doc_manager.JournalArticle,
                    managers.doc_manager.Copy,
                    managers.user_manager.User,
                    managers.group_manager.Group,
                    managers.booking_system.History], safe=True)

