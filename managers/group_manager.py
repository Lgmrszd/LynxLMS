from peewee import *
from dbconfig import BaseModel


class Group(BaseModel):
    id = PrimaryKeyField()
    name = TextField()
    checkout_time = SmallIntegerField()
