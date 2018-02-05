from peewee import *

db = SqliteDatabase('data/database.db')
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


def custom_db(dbfile):
    db.init(dbfile)
