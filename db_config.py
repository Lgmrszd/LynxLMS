import managers.doc_manager
import managers.user_manager
import managers.group_manager
import managers.booking_system
from db_connect import db


def initialize_db():
    # Creating tables
    db.create_tables([managers.doc_manager.Book,
                      managers.doc_manager.AVMaterial,
                      managers.doc_manager.JournalArticle,
                      managers.doc_manager.Copy,
                      managers.user_manager.User,
                      managers.group_manager.Group,
                      managers.booking_system.History], safe=True)


def drop_db():
    db.drop_tables([managers.doc_manager.Book,
                    managers.doc_manager.AVMaterial,
                    managers.doc_manager.JournalArticle,
                    managers.doc_manager.Copy,
                    managers.user_manager.User,
                    managers.group_manager.Group,
                    managers.booking_system.History], safe=True)
