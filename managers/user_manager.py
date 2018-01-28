from peewee import *
from dbconfig import BaseModel


class User(BaseModel):
    card_id = IntegerField()
    name = TextField()
    surname = TextField()
    address = TextField()
    phone = BigIntegerField()
