from peewee import *
from os.path import exists
from os import makedirs

if not exists("./data"):
    makedirs("./data")


db = SqliteDatabase("./data/database.db")
db.connect()


class BaseModel(Model):
    class Meta:
        database = db


def custom_db(dbfile):
    db.init(dbfile)
