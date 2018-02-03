import managers.doc_manager
import managers.user_manager
import managers.group_manager
from db_connect import db


def initialize_db():
    # Creating tables
    db.create_tables([managers.doc_manager.Book,
                      managers.doc_manager.AVMaterial,
                      managers.doc_manager.JournalArticle,
                      managers.user_manager.User,
                      managers.group_manager.Group], safe=True)


def drop_db():
    db.drop_tables([managers.doc_manager.Book,
                    managers.doc_manager.AVMaterial,
                    managers.doc_manager.JournalArticle,
                    managers.user_manager.User,
                    managers.group_manager.Group], safe=True)
