import peewee as pw
from managers.group_manager import Group
from dbconfig import BaseModel


class User(BaseModel):
    card_id = pw.IntegerField(primary_key=True)
    name = pw.TextField()
    surname = pw.TextField()
    address = pw.TextField()
    phone = pw.BigIntegerField()
    group = pw.ForeignKeyField(Group, related_name="users")
