from peewee import *
import managers.doc_manager
import managers.user_manager
import managers.group_manager

db = SqliteDatabase('data/database.db')


class BaseModel(Model):
    class Meta:
        database = db


def initialize_db():
    # Connecting database
    db.connect()

    # Creating tables
    db.create_tables([managers.doc_manager.Book,
        managers.doc_manager.AV_material,
        managers.doc_manager.Journal_article,
        managers.user_manager.User,
        managers.group_manager.Group], safe=True)


def drop_db():
    db.connect()

    db.drop_tables([managers.doc_manager.Book,
        managers.doc_manager.AV_material,
        managers.doc_manager.Journal_article,
        managers.user_manager.User,
        managers.group_manager.Group], safe=True)
