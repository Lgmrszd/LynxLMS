from peewee import *

db = SqliteDatabase(None)


class BaseModel(Model):
    class Meta:
        database = db


def custom_db(dbfile):
    db.init(dbfile)
