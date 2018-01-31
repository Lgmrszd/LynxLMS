from peewee import *

db = SqliteDatabase('data/database.db')


class BaseModel(Model):
    class Meta:
        database = db
