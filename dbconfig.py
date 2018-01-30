from peewee import *

db = SqliteDatabase('../database/database.db')


class BaseModel(Model):
    class Meta:
        database = db

