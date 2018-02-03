from peewee import *
from db_connect import BaseModel


class Group(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    checkout_time = SmallIntegerField()
